# mlopscli/pipeline.py
import subprocess
from pathlib import Path


def topological_sort(steps: dict):
    from collections import defaultdict, deque

    graph = defaultdict(list)
    indegree = defaultdict(int)

    for name, step in steps.items():
        for dep in step.get("depends_on", []):
            graph[dep].append(name)
            indegree[name] += 1

    queue = deque([name for name in steps if indegree[name] == 0])
    sorted_steps = []

    while queue:
        node = queue.popleft()
        sorted_steps.append(steps[node])
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(sorted_steps) != len(steps):
        raise ValueError("Cycle detected in job dependencies!")

    return sorted_steps


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


def execute_scripts(steps_dict):
    """Execute the job steps in the correct order (topologically sorted)."""
    sorted_steps = topological_sort(steps_dict)

    for step in sorted_steps:
        name = step["name"]
        script = step["script"]
        requirements = step.get("requirements")

        print(f"\n🔧 Running step: {name} ({script})")

        # Check if the script exists
        script_path = Path(script)
        if not script_path.exists():
            raise FileNotFoundError(f"❌ Script not found: {script_path.resolve()}")

        # Set up the virtual environment for this step and get the python executable
        python_exe = setup_virtualenv(name, requirements)

        # Run the script in the virtual environment
        result = subprocess.run(
            [str(python_exe), str(script_path)], capture_output=True, text=True
        )

        # Handle the result
        if result.returncode != 0:
            print(f"❌ Step '{name}' failed.")
            print(result.stderr)
            break
        else:
            print(f"✅ Step '{name}' completed.")
            print(result.stdout)
