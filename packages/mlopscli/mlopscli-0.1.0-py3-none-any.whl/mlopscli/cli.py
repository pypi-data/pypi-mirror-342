# mlopscli/cli.py
import typer
from pathlib import Path
from mlopscli.runner import run_pipeline
import shutil

app = typer.Typer()


@app.command()
def execute(
    job_name: str = typer.Option(
        ..., "--job", help="Job name (e.g., prepare_train_pipeline)"
    ),
    job_config: Path = typer.Option(..., "--job_config", help="Path to job_order.yaml"),
    render_dag: bool = typer.Option(
        True, "--render_dag/--no-render_dag", help="Render DAG to image"
    ),
):
    """Runs the jobs as a pipeline and renders DAG if requested."""
    typer.echo(f"Running job: {job_name}")
    run_pipeline(job_name, job_config, render_dag)


@app.command()
def cleanup(step_name: str = None, all: bool = False):
    """Clean up virtual environments for pipeline steps."""
    if all:
        # Clean all virtual environments
        envs_dir = Path(".mlopscli_envs")
        if envs_dir.exists():
            for env in envs_dir.iterdir():
                if env.is_dir():
                    print(f"🧹 Cleaning environment: {env.name}")
                    shutil.rmtree(env)
        else:
            print("❌ No environments to clean.")
    elif step_name:
        # Clean the specific environment for the given step
        env_dir = Path(".mlopscli_envs") / step_name
        if env_dir.exists():
            print(f"🧹 Cleaning environment for step: {step_name}")
            shutil.rmtree(env_dir)
        else:
            print(f"❌ Environment for step '{step_name}' does not exist.")
    else:
        print(
            "❌ Please provide either a step name or use the '--all' flag to clean all environments."
        )


if __name__ == "__main__":
    app()
