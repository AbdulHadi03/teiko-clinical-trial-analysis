import os
import sqlite3
import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "clinical_trial.db"
OUTPUT_DIR = "outputs"


def create_summary_table(conn):
    query = """
        SELECT 
            s.sample_id AS sample,
            s.project,
            s.subject_id,
            s.condition,
            s.sex,
            s.treatment,
            s.response,
            s.sample_type,
            s.time_from_treatment_start,
            c.population,
            c.count
        FROM samples s
        JOIN cell_counts c
            ON s.sample_id = c.sample_id
    """

    df = pd.read_sql(query, conn)

    total_counts = (
        df.groupby("sample")["count"]
        .sum()
        .reset_index()
        .rename(columns={"count": "total_count"})
    )

    df = df.merge(total_counts, on="sample")
    df["percentage"] = (df["count"] / df["total_count"]) * 100

    summary = df[
        ["sample", "total_count", "population", "count", "percentage"]
    ]

    summary.to_csv(f"{OUTPUT_DIR}/summary_table.csv", index=False)

    df.to_csv(f"{OUTPUT_DIR}/summary_table_with_metadata.csv", index=False)

    return df


def run_statistical_analysis(summary_df):
    filtered = summary_df[
        (summary_df["condition"] == "melanoma")
        & (summary_df["treatment"] == "miraclib")
        & (summary_df["sample_type"] == "PBMC")
        & (summary_df["response"].isin(["yes", "no"]))
    ]

    results = []

    for population in filtered["population"].unique():
        pop_df = filtered[filtered["population"] == population]

        responders = pop_df[pop_df["response"] == "yes"]["percentage"]
        non_responders = pop_df[pop_df["response"] == "no"]["percentage"]

        if len(responders) > 0 and len(non_responders) > 0:
            stat, p_value = mannwhitneyu(
                responders,
                non_responders,
                alternative="two-sided"
            )

            results.append({
                "population": population,
                "responder_mean_percentage": responders.mean(),
                "non_responder_mean_percentage": non_responders.mean(),
                "p_value": p_value,
                "significant": p_value < 0.05
            })

    stats_df = pd.DataFrame(results)
    stats_df.to_csv(f"{OUTPUT_DIR}/significant_populations.csv", index=False)

    plt.figure(figsize=(10, 6))
    sns.boxplot(
        data=filtered,
        x="population",
        y="percentage",
        hue="response"
    )
    plt.title("Cell Population Frequencies: Responders vs Non-Responders")
    plt.xlabel("Cell Population")
    plt.ylabel("Relative Frequency (%)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/responder_vs_nonresponder_boxplot.png")
    plt.close()

    return stats_df


def run_subset_analysis(conn):
    query = """
        SELECT 
            s.project,
            s.subject_id,
            s.condition,
            s.sex,
            s.treatment,
            s.response,
            s.sample_type,
            s.time_from_treatment_start,
            c.population,
            c.count
        FROM samples s
        JOIN cell_counts c
            ON s.sample_id = c.sample_id
        WHERE s.condition = 'melanoma'
          AND s.sample_type = 'PBMC'
          AND s.treatment = 'miraclib'
          AND s.time_from_treatment_start = 0
    """

    subset = pd.read_sql(query, conn)

    project_counts = (
        subset.drop_duplicates("subject_id")
        .groupby("project")
        .size()
        .reset_index(name="sample_count")
    )

    response_counts = (
        subset.drop_duplicates("subject_id")
        .groupby("response")
        .size()
        .reset_index(name="subject_count")
    )

    sex_counts = (
        subset.drop_duplicates("subject_id")
        .groupby("sex")
        .size()
        .reset_index(name="subject_count")
    )

    avg_b_cells = subset[
        (subset["condition"] == "melanoma")
        & (subset["sex"] == "M")
        & (subset["response"] == "yes")
        & (subset["time_from_treatment_start"] == 0)
        & (subset["population"] == "b_cell")
    ]["count"].mean()

    avg_b_cells_df = pd.DataFrame([{
        "group": "melanoma_male_responders_time_0",
        "average_b_cell_count": round(avg_b_cells, 2)
    }])

    project_counts.to_csv(f"{OUTPUT_DIR}/baseline_project_counts.csv", index=False)
    response_counts.to_csv(f"{OUTPUT_DIR}/baseline_response_counts.csv", index=False)
    sex_counts.to_csv(f"{OUTPUT_DIR}/baseline_sex_counts.csv", index=False)
    avg_b_cells_df.to_csv(f"{OUTPUT_DIR}/avg_b_cells_male_responders.csv", index=False)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    summary_df = create_summary_table(conn)
    stats_df = run_statistical_analysis(summary_df)
    run_subset_analysis(conn)

    conn.close()

    print("Pipeline completed successfully.")
    print("Generated outputs in the outputs/ folder.")
    print(stats_df)


if __name__ == "__main__":
    main()
