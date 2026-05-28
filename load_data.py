import sqlite3
import pandas as pd

DB_PATH = "clinical_trial.db"
CSV_PATH = "data/cell-count.csv"

POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS cell_counts")
    cursor.execute("DROP TABLE IF EXISTS samples")

    cursor.execute("""
        CREATE TABLE samples (
            sample_id TEXT PRIMARY KEY,
            project TEXT,
            subject_id TEXT,
            condition TEXT,
            age INTEGER,
            sex TEXT,
            treatment TEXT,
            response TEXT,
            sample_type TEXT,
            time_from_treatment_start INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE cell_counts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sample_id TEXT,
            population TEXT,
            count INTEGER,
            FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
        )
    """)

    conn.commit()


def load_data(conn):
    df = pd.read_csv(CSV_PATH)

    sample_rows = df[
        [
            "sample",
            "project",
            "subject",
            "condition",
            "age",
            "sex",
            "treatment",
            "response",
            "sample_type",
            "time_from_treatment_start",
        ]
    ].rename(columns={
        "sample": "sample_id",
        "subject": "subject_id",
    })

    sample_rows.to_sql("samples", conn, if_exists="append", index=False)

    count_rows = df.melt(
        id_vars=["sample"],
        value_vars=POPULATIONS,
        var_name="population",
        value_name="count"
    ).rename(columns={"sample": "sample_id"})

    count_rows.to_sql("cell_counts", conn, if_exists="append", index=False)


def main():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    load_data(conn)
    conn.close()
    print(f"Database created successfully: {DB_PATH}")


if __name__ == "__main__":
    main()
