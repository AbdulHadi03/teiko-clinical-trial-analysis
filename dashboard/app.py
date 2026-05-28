import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Clinical Trial Dashboard",
    layout="wide"
)

st.title("Clinical Trial Immune Cell Analysis Dashboard")

st.header("Summary Table")

summary_df = pd.read_csv("outputs/summary_table_with_metadata.csv")

st.dataframe(summary_df)

st.header("Statistical Analysis")

stats_df = pd.read_csv("outputs/significant_populations.csv")

st.dataframe(stats_df)

st.subheader("Responder vs Non-Responder Boxplot")

image = Image.open("outputs/responder_vs_nonresponder_boxplot.png")
st.image(image)

st.header("Baseline Subset Analysis")

project_counts = pd.read_csv("outputs/baseline_project_counts.csv")
response_counts = pd.read_csv("outputs/baseline_response_counts.csv")
sex_counts = pd.read_csv("outputs/baseline_sex_counts.csv")
avg_b_cells = pd.read_csv("outputs/avg_b_cells_male_responders.csv")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Project Counts")
    st.dataframe(project_counts)

    st.subheader("Response Counts")
    st.dataframe(response_counts)

with col2:
    st.subheader("Sex Counts")
    st.dataframe(sex_counts)

    st.subheader("Average B Cells")
    st.dataframe(avg_b_cells)

st.sidebar.header("Filters")

condition_filter = st.sidebar.multiselect(
    "Condition",
    summary_df["condition"].unique(),
    default=summary_df["condition"].unique()
)

response_filter = st.sidebar.multiselect(
    "Response",
    summary_df["response"].unique(),
    default=summary_df["response"].unique()
)

filtered_df = summary_df[
    (summary_df["condition"].isin(condition_filter))
    & (summary_df["response"].isin(response_filter))
]

st.header("Filtered Data")

st.dataframe(filtered_df)
