from dagster import op, job, Definitions
import subprocess
import os


# =====================
# SCRAPE
# =====================
@op
def scrape_telegram_data():
    result = subprocess.run(
        ["python", "scripts/scraper.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return "scraped"


# =====================
# LOAD
# =====================
@op
def load_raw_to_postgres():
    result = subprocess.run(
        ["python", "scripts/load_to_postgres.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return "loaded"


# =====================
# DBT
# =====================
@op
def run_dbt_transformations():
    result = subprocess.run(
        ["dbt", "run"],
        cwd="medical_warehouse",
        capture_output=True,
        text=True,
        env={**os.environ},
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return "dbt_done"


# =====================
# YOLO
# =====================
@op
def run_yolo_enrichment():
    result = subprocess.run(
        ["python", "src/yolo_detect.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Exception(result.stderr)

    return "yolo_done"


# =====================
# JOB (PIPELINE)
# =====================
@job
def medical_telegram_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()


# =====================
# IMPORTANT ENTRYPOINT
# =====================
defs = Definitions(
    jobs=[medical_telegram_pipeline]
)