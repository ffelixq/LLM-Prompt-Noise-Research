from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="LLM PromptNoise", layout="wide")
st.title("LLM PromptNoise Benchmark")

default_path = Path("results/tables/pilot_summary.csv")
uploaded = st.file_uploader("Upload an aggregate summary CSV", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
elif default_path.exists():
    df = pd.read_csv(default_path)
else:
    st.info("Run the benchmark analysis or upload a summary CSV to explore results.")
    st.stop()

models = sorted(df["model_config_id"].dropna().unique())
selected = st.multiselect("Models", models, default=models)
view = df[df["model_config_id"].isin(selected)].copy()

if "accuracy" in view:
    fig = px.line(
        view,
        x="condition",
        y="accuracy",
        color="model_config_id",
        facet_col="task_type",
        markers=True,
        title="Accuracy by prompt condition",
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    if "avg_input_tokens" in view:
        fig = px.bar(
            view,
            x="condition",
            y="avg_input_tokens",
            color="model_config_id",
            barmode="group",
            title="Average input tokens",
        )
        st.plotly_chart(fig, use_container_width=True)

with right:
    if "robustness_ratio" in view:
        fig = px.bar(
            view,
            x="condition",
            y="robustness_ratio",
            color="model_config_id",
            barmode="group",
            title="Robustness ratio vs clean",
        )
        st.plotly_chart(fig, use_container_width=True)

st.dataframe(view, use_container_width=True)
