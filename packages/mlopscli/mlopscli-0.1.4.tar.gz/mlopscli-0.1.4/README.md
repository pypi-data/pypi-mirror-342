# mlopscli 🚀

A CLI tool to turn DS Python scripts + YAML config into an executable ML pipeline.

## Usage

1. Write your scripts focussing on different steps in ML Lifecyle (`data_prep.py`, `train_model.py`, `evaluate_model.py`)
2. Define them in a `job_order.yaml` with the dependencies.
3. Install the mlops cli : `pip install mlopscli`
4. Run the CLI command.

#### Commands Available

1. Spin up a streamlit dashboard where the metadata of all the runs will be available.

```bash
mlopscli dashboard
```

2. Dry Run the pipeline to ensure Job Config is valid. Validations like dependencies, file paths are checked during dry run

```bash
mlopscli dry-run --job prepare_train_pipeline --job_config job_order.yaml
```

3. Execute the pipeline and get results

```bash
mlopscli execute --job prepare_train_pipeline --job_config job_order.yaml --observe
```

`--observe` : If passed, the resource consumption like CPU/Memory usage will be calculated for each step.


> ⚠️ **NOTE** : 
>  - If the environments already exists, it is not recreated.
>  - Once the DAG is prepared, the steps in the same level are ran in parallel.

4. Clean up Environments

```bash
mlopscli cleanup --step-name train
```

`--step-name` : If passed, the environment associated with the input step is deleted.

```bash
mlopscli cleanup --all
```

`--all` : If passed, all the environments are cleaned up.


**Quick Demo**

[![Watch the demo](https://img.youtube.com/vi/MFBbSA-SHFU/hqdefault.jpg)](https://www.youtube.com/watch?v=MFBbSA-SHFU)

