# mlopscli/runner.py
from mlopscli.parser import load_job_config
from mlopscli.pipeline import execute_scripts
from pathlib import Path
from mlopscli.dag_visualizer import visualize_dag

from pathlib import Path


def dry_run_pipeline(job_name: str, job_config: Path):
    """Simulate running the pipeline steps without actually executing them."""
    _, steps = load_job_config(job_config)

    print(f"\n🧪 Dry Run for Pipeline: {job_name}")
    print(f"📄 Pipeline Configuration: {job_config.resolve()}")

    step_names = {step.get("name") for step in steps.values()}
    missing_dependencies = []
    missing_scripts = []
    missing_requirements = []

    for step in steps.values():
        name = step.get("name")
        script = step.get("script")
        requirements = step.get("requirements", None)
        depends_on = step.get("depends_on", [])

        print(f"\n🔍 Step: {name}")
        print(f"  📜 Script: {script}")
        print(f"  📦 Requirements: {requirements or 'N/A'}")
        print(f"  🔗 Depends on: {', '.join(depends_on) if depends_on else 'None'}")

        # Validate script path
        if not Path(script).exists():
            missing_scripts.append((name, script))

        # Validate requirements path (if provided)
        if requirements and not Path(requirements).exists():
            missing_requirements.append((name, requirements))

        # Validate depends_on steps
        for dep in depends_on:
            if dep not in step_names:
                missing_dependencies.append((name, dep))

    if missing_scripts or missing_requirements or missing_dependencies:
        print("\n❌ Issues detected during dry run:")

        if missing_scripts:
            print("\n🚫 Missing Scripts:")
            for step, path in missing_scripts:
                print(f"  - Step '{step}': script path not found -> {path}")

        if missing_requirements:
            print("\n🚫 Missing Requirements:")
            for step, path in missing_requirements:
                print(f"  - Step '{step}': requirements path not found -> {path}")

        if missing_dependencies:
            print("\n🚫 Invalid Dependencies:")
            for step, dep in missing_dependencies:
                print(f"  - Step '{step}' depends on undefined step '{dep}'")

        print("\n💥 Dry run failed due to the above errors.")
    else:
        print(
            "\n✅ Dry run completed successfully. All paths and dependencies look good!"
        )


def run_pipeline(
    job_name: str, job_config: Path, render_dag: bool = True, observe: bool = False
):
    pipeline_name, step_dict = load_job_config(job_config)
    print(f"Starting pipeline: {pipeline_name} under job {job_name}")

    if render_dag:
        visualize_dag(job_name, step_dict)

    execute_scripts(job_name=job_name, steps_dict=step_dict, observe=observe)
