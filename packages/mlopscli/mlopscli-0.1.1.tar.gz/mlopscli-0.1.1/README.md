# mlopscli 🚀

A CLI tool to turn DS Python scripts + YAML config into an executable ML pipeline.

## Usage

1. Write your scripts (`data_prep.py`, `train_model.py`, `evaluate_model.py`)
2. Define them in a `job_order.yaml` with the dependencies.
3. Install the mlops cli : `pip install mlopscli`
4. Run the command: `mlopscli execute --job prepare_train_pipeline --job_config job_order.yaml`
