# Clinical Trial Immune Cell Analysis

## Overview

This project analyzes immune cell population data from a clinical trial dataset using Python, SQLite, statistical analysis, and Streamlit.

The project includes:

- A SQLite database schema for storing sample metadata and immune cell counts
- A data loading pipeline
- Statistical analysis comparing responders and non-responders
- Automated output generation
- An interactive dashboard

---

## Tech Stack

- Python
- SQLite
- pandas
- scipy
- matplotlib
- seaborn
- Streamlit

---

## Repository Structure

```text
.
├── data/
│   └── cell-count.csv
├── dashboard/
│   └── app.py
├── outputs/
│   ├── avg_b_cells_male_responders.csv
│   ├── baseline_project_counts.csv
│   ├── baseline_response_counts.csv
│   ├── baseline_sex_counts.csv
│   ├── responder_vs_nonresponder_boxplot.png
│   ├── significant_populations.csv
│   ├── summary_table.csv
│   └── summary_table_with_metadata.csv
├── load_data.py
├── run_pipeline.py
├── requirements.txt
├── Makefile
├── clinical_trial.db
└── README.md
```
---

## Setup

Install dependencies:

bash make setup 

---

## Run the Pipeline

Execute the full pipeline:

bash make pipeline 

This command:

1. Creates the SQLite database
2. Loads all rows from cell-count.csv
3. Generates the summary frequency table
4. Runs statistical analysis
5. Generates output tables and plots
6. Runs baseline subset analysis

---

## Run the Dashboard

Start the Streamlit dashboard:

bash make dashboard 

Dashboard URL:

text http://localhost:8501 

If running inside GitHub Codespaces, open the forwarded Streamlit port.

---

## Database Schema

The project uses a normalized relational schema with two tables.

### samples

Stores metadata for each biological sample.

Columns:

- sample_id
- project
- subject_id
- condition
- age
- sex
- treatment
- response
- sample_type
- time_from_treatment_start

### cell_counts

Stores immune population counts in long format.

Columns:

- id
- sample_id
- population
- count

Each row represents one immune cell population for one sample.

---

## Schema Rationale

The original CSV stores immune populations as separate columns. The pipeline transforms this into a normalized long-format structure.

Advantages of this design:

- Easier aggregation and statistical analysis
- More scalable for future immune populations
- Cleaner relational modeling
- Reduced redundancy
- Better support for large-scale analytics

This schema can scale effectively to hundreds of projects and thousands of samples.

---

## Part 1: Data Management

load_data.py:

- Creates the SQLite database
- Creates the schema
- Loads all rows from the CSV file

Run directly with:

bash python load_data.py 

This generates:

text clinical_trial.db 

---

## Part 2: Relative Frequency Summary

The pipeline computes:

- Total immune cell count per sample
- Relative frequency of each immune population

Output:

text outputs/summary_table.csv 

Columns:

- sample
- total_count
- population
- count
- percentage

---

## Part 3: Statistical Analysis

The analysis compares:

- melanoma PBMC samples
- treated with miraclib
- responders vs non-responders

Statistical method:

- Mann-Whitney U test

Generated outputs:

text outputs/significant_populations.csv outputs/responder_vs_nonresponder_boxplot.png 

Result:

cd4_t_cell showed a statistically significant difference between responders and non-responders using a threshold of p < 0.05.

---

## Part 4: Baseline Subset Analysis

The subset includes samples where:

- condition = melanoma
- sample_type = PBMC
- treatment = miraclib
- time_from_treatment_start = 0

The pipeline reports:

- Number of baseline samples from each project
- Number of responder/non-responder subjects
- Number of male/female subjects
- Average B-cell count for melanoma male responders at time 0

Generated outputs:

text outputs/baseline_project_counts.csv outputs/baseline_response_counts.csv outputs/baseline_sex_counts.csv outputs/avg_b_cells_male_responders.csv 

Average B-cell count for melanoma male responders at time 0:

text 10401.28 

---

## Code Structure

### load_data.py

Responsible for:

- Creating the SQLite schema
- Reading the CSV file
- Loading metadata into the samples table
- Loading immune counts into the cell_counts table

### run_pipeline.py

Responsible for:

- Generating summary tables
- Running statistical analysis
- Creating plots
- Running subset analysis
- Saving output files

### dashboard/app.py

Responsible for:

- Displaying analytical outputs
- Showing statistical visualizations
- Providing interactive filtering

---

## Makefile Targets

The root Makefile includes:

bash make setup make pipeline make dashboard 

These commands allow the project to be reproduced locally or in GitHub Codespaces.
