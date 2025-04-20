# mlopscli/runner.py
from mlopscli.parser import load_job_config
from mlopscli.pipeline import execute_scripts
from pathlib import Path
from mlopscli.dag_visualizer import visualize_dag


def run_pipeline(job_name: str, job_config: Path, render_dag: bool = True):
    pipeline_name, step_dict = load_job_config(job_config)
    print(f"Starting pipeline: {pipeline_name} under job {job_name}")

    if render_dag:
        visualize_dag(pipeline_name, step_dict)

    execute_scripts(step_dict)
