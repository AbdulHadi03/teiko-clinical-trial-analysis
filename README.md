Clinical Trial Immune Cell Analysis

Overview

This project analyzes immune cell population data from a clinical trial dataset using Python, SQLite, statistical analysis, and an interactive Streamlit dashboard.

The pipeline:

* Loads clinical trial data into a relational SQLite database
* Computes relative immune cell frequencies
* Performs statistical analysis comparing responders vs non-responders
* Generates visualizations
* Provides an interactive dashboard for exploration

⸻

Tech Stack

* Python
* SQLite
* pandas
* scipy
* seaborn
* matplotlib
* Streamlit

⸻

Project Structure

teiko-technical/
│
├── data/
│   └── cell-count.csv
│
├── outputs/
│   ├── summary_table.csv
│   ├── summary_table_with_metadata.csv
│   ├── significant_populations.csv
│   ├── responder_vs_nonresponder_boxplot.png
│   ├── baseline_project_counts.csv
│   ├── baseline_response_counts.csv
│   ├── baseline_sex_counts.csv
│   └── avg_b_cells_male_responders.csv
│
├── dashboard/
│   └── app.py
│
├── load_data.py
├── run_pipeline.py
├── requirements.txt
├── Makefile
├── clinical_trial.db
└── README.md

⸻

Database Schema Design

The database uses a normalized relational schema consisting of two tables.

samples table

Stores metadata for each biological sample:

* sample_id
* project
* subject_id
* condition
* age
* sex
* treatment
* response
* sample_type
* time_from_treatment_start

cell_counts table

Stores immune population counts in long-format form:

* sample_id
* population
* count

This schema design was chosen because it scales efficiently for future analytical workflows.

Advantages include:

* New immune populations can be added without schema changes
* Simplified aggregation and statistical analysis
* Reduced redundancy through normalization
* Easier querying for downstream analytics
* Better scalability for hundreds of projects and thousands of samples

This design supports future extensions such as additional immune populations, new treatments, or more advanced analytical pipelines.

⸻

Pipeline Execution

Install Dependencies

make setup

Run Complete Pipeline

make pipeline

This command automatically:

* Creates the SQLite database
* Loads CSV data into the database
* Generates summary tables
* Performs statistical analysis
* Produces plots and output files

Run Dashboard

make dashboard

This launches the interactive Streamlit dashboard locally.

⸻

Statistical Analysis

The statistical analysis compares melanoma PBMC samples treated with miraclib between responders and non-responders.

The following filtering criteria were applied:

* condition = melanoma
* treatment = miraclib
* sample_type = PBMC

A Mann-Whitney U test was used to compare relative frequencies between groups because immune cell distributions may not follow normal distributions.

Significance threshold:

p < 0.05

The analysis identified statistically significant differences in immune cell population frequencies between responders and non-responders.

⸻

Outputs

Generated outputs include:

* summary_table.csv
* summary_table_with_metadata.csv
* significant_populations.csv
* responder_vs_nonresponder_boxplot.png
* baseline_project_counts.csv
* baseline_response_counts.csv
* baseline_sex_counts.csv
* avg_b_cells_male_responders.csv

⸻

Dashboard Features

The Streamlit dashboard provides:

* Interactive data exploration
* Statistical result visualization
* Boxplot comparison of responders vs non-responders
* Baseline subset analysis
* Interactive filtering functionality

⸻

Code Structure

The project is organized into separate stages for maintainability and reproducibility.

load_data.py

Responsible for:

* Creating the SQLite schema
* Loading CSV data into the database
* Transforming immune population columns into normalized relational format

run_pipeline.py

Responsible for:

* Generating summary tables
* Computing relative frequencies
* Performing statistical analysis
* Creating plots
* Running subset analyses
* Saving analytical outputs

dashboard/app.py

Responsible for:

* Displaying results interactively using Streamlit
* Providing filtering and visualization capabilities

This modular structure improves readability, maintainability, and scalability for future development.

⸻

Dashboard Link

Local dashboard can be started using:

make dashboard

⸻

Future Improvements

Potential future extensions include:

* Additional statistical methods
* Machine learning prediction models
* Multi-treatment comparison workflows
* Time-series immune trajectory analysis
* Deployment to cloud infrastructure
* Automated testing and CI/CD integration

⸻