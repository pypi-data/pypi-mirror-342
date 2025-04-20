import streamlit as st
import json
from pathlib import Path

ARTIFACTS_DIR = Path("mlops_artifacts")

st.set_page_config(page_title="MLOps CLI Dashboard", layout="wide")
st.title("🚀 MLOps CLI Dashboard")

if not ARTIFACTS_DIR.exists():
    st.warning("No job runs found in `mlops_artifacts/`.")
    st.stop()

# List all runs (sorted latest first)
runs = sorted(ARTIFACTS_DIR.glob("run_*"), reverse=True)

selected_run = st.selectbox("📁 Select a job run:", runs)
pipeline_name = ""

if selected_run:
    st.subheader(f"🧾 Run: `{selected_run.name}`")

    # Load metadata.json
    metadata_path = selected_run / "metadata.json"
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)

        pipeline_name = metadata["job_name"]
        st.markdown(f"**Pipeline:** `{pipeline_name}`")
        st.markdown(f"**Started at:** `{metadata['timestamp']}`")

        st.subheader("🛠 Steps")
        for step in metadata.get("steps", []):
            with st.expander(f"🔹 {step['name']} ({step['status']})"):
                st.markdown(f"**Script:** `{step['script']}`")
                st.markdown(f"**Duration:** {step['duration']} seconds")
                log_path = selected_run / "logs" / f"{step['name']}.log"
                if log_path.exists():
                    with open(log_path) as log_file:
                        st.code(log_file.read(), language="bash")
                else:
                    st.text("🚫 No logs found for this step.")

    else:
        st.error("⚠️ metadata.json not found for this run.")

    # Show DAG image
    dag_path = selected_run / f"{pipeline_name}_dag.png"
    if dag_path.exists():
        st.subheader("📈 DAG")
        st.image(str(dag_path))
    else:
        st.warning("No DAG image found.")
