# mlopscli/pipeline.py
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from threading import Thread
import networkx as nx
import psutil, time, json
from mlopscli.constants import ARTIFACTS_DIRECTORY


def write_metadata(run_dir, job_name, steps, timestamp):
    """Writes the metadata to a JSON file in the run directory."""
    metadata = {"job_name": job_name, "timestamp": timestamp, "steps": steps}
    metadata_path = run_dir / "metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=4)


def monitor_process(proc, metrics):
    p = psutil.Process(proc.pid)
    mem_usage = []
    cpu_usage = []

    while proc.poll() is None:
        try:
            mem = p.memory_info().rss / (1024 * 1024)  # in MB
            cpu = p.cpu_percent(interval=0.2)
            mem_usage.append(mem)
            cpu_usage.append(cpu)
        except psutil.NoSuchProcess:
            break

    metrics["memory"] = mem_usage
    metrics["cpu"] = cpu_usage


def setup_virtualenv(step_name: str, requirements_path: str):
    """Creates and sets up a virtual environment for the given step."""
    env_dir = Path(".mlopscli_envs") / step_name
    python_bin = env_dir / "bin" / "python"

    # If virtualenv doesn't exist, create it
    if not python_bin.exists():
        print(f"📦 Creating virtual environment for step: {step_name}")
        subprocess.run(["python3", "-m", "venv", str(env_dir)], check=True)

        # Upgrade pip
        subprocess.run(
            [str(python_bin), "-m", "pip", "install", "--upgrade", "pip"], check=True
        )

        # Install dependencies for the step
        if requirements_path and Path(requirements_path).exists():
            print(f"📄 Installing requirements from {requirements_path}")
            subprocess.run(
                [str(python_bin), "-m", "pip", "install", "-r", requirements_path],
                check=True,
            )
        else:
            print(f"❌ Requirements file path does not exists : {requirements_path}")
    else:
        print(f"✅ Using cached environment for {step_name}")

    return python_bin


def build_dependency_graph(steps_dict):
    G = nx.DiGraph()
    for step_name, step_info in steps_dict.items():
        G.add_node(step_name, info=step_info)
        for dep in step_info.get("depends_on", []):
            G.add_edge(dep, step_name)
    return G


def execute_scripts(job_name, steps_dict, max_workers=4, observe=False):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    G = build_dependency_graph(steps_dict)
    completed = set()
    running_futures = {}
    run_dir = Path(ARTIFACTS_DIRECTORY)
    run_dir.mkdir(parents=True, exist_ok=True)
    steps_metadata = []

    def run_step(step_name, observe):
        start = time.time()
        step = steps_dict[step_name]
        name = step["name"]
        script = step["script"]
        requirements = step.get("requirements")

        print(f"\n🔧 Running step: {name} ({script})")
        script_path = Path(script)
        if not script_path.exists():
            raise FileNotFoundError(f"❌ Script not found: {script_path.resolve()}")

        python_exe = setup_virtualenv(name, requirements)

        if observe:
            metrics = {}
            result = subprocess.Popen([str(python_exe), str(script_path)])
            monitor = Thread(target=monitor_process, args=(result, metrics))
            monitor.start()
            result.wait()
            monitor.join()
        else:
            result = subprocess.run(
                [str(python_exe), str(script_path)],
                capture_output=True,
                text=True,
            )

        end = time.time()
        duration = end - start

        step_metadata = {
            "name": name,
            "status": "success" if result.returncode == 0 else "failed",
            "duration": duration,
            "script": str(script_path),
        }

        steps_metadata.append(step_metadata)

        if result.returncode != 0:
            raise RuntimeError(f"❌ Step '{name}' failed:\n{result.stderr}")

        print(f"✅ Step '{name}' completed in {duration:.2f}s")

        if observe:
            peak_mem = max(metrics["memory"]) if metrics["memory"] else 0
            avg_cpu = sum(metrics["cpu"]) / len(metrics["cpu"]) if metrics["cpu"] else 0
            print(f"🧠 Peak memory for step {name}: {peak_mem:.2f} MB")
            print(f"⚙️ Avg CPU for step {name}: {avg_cpu:.2f}%")
        else:
            print(result.stdout)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while len(completed) < len(G.nodes):
            # Get new ready steps (not completed, not already running)
            ready_steps = [
                node
                for node in G.nodes
                if node not in completed
                and node not in running_futures.values()
                and all(pred in completed for pred in G.predecessors(node))
            ]

            # Submit new ready steps
            for step_name in ready_steps:
                future = executor.submit(run_step, step_name, observe)
                running_futures[future] = step_name

            if not running_futures:
                raise RuntimeError("⚠️ Deadlock detected or no runnable steps found.")

            # Process completed futures
            done, _ = wait(running_futures.keys(), return_when=FIRST_COMPLETED)
            for future in done:
                step_name = running_futures.pop(future)
                try:
                    future.result()
                    completed.add(step_name)
                except Exception as e:
                    print(f"❌ Error in step '{step_name}': {e}")
                    executor.shutdown(wait=False)
                    return  # Exit early on error

    write_metadata(run_dir, job_name, steps_metadata, timestamp)
