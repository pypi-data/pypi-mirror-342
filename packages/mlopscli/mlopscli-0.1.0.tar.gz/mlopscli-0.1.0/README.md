# mlopscli 🚀

A CLI tool to turn DS Python scripts + YAML config into an executable ML pipeline.

## Usage

1. Write your scripts (`data_prep.py`, `train_model.py`, `evaluate_model.py`)
2. Define them in a `job_order.yaml`
3. Run:

```bash
python -m mlopscli.cli --job "prepare_train_pipeline" --job_config job_examples/job_order.yaml
