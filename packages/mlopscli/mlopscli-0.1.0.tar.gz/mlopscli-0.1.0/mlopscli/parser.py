# mlopscli/parser.py
import yaml
from pathlib import Path


def load_job_config(config_path: Path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    pipeline_name = config.get("pipeline_name", "default_pipeline")
    steps = config.get("steps", [])

    if not steps:
        raise ValueError("No steps found in job config!")

    step_dict = {}
    for step in steps:
        print(f"Step Details : {step}")
        name = step["name"]
        script = Path(step["script"])
        depends_on = step.get("depends_on", [])
        requirements = (
            Path(step.get("requirements")) if step.get("requirements") else None
        )

        if not script.exists():
            raise FileNotFoundError(f"Script not found: {script}")
        step_dict[name] = {
            "name": name,
            "script": script,
            "depends_on": depends_on,
            "requirements": requirements,
        }

    return pipeline_name, step_dict
