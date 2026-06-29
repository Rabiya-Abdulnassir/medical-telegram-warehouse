from dagster import op, job, Failure, Definitions, ScheduleDefinition
import subprocess
import os


@op
def scrape_telegram_data():
    result = subprocess.run(
        ["python", "scripts/scraper.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Failure(result.stderr)

    return "scraped"


@op
def load_raw_to_postgres():
    result = subprocess.run(
        ["python", "scripts/load_to_postgres.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Failure(result.stderr)

    return "loaded"


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
        raise Failure(result.stderr)

    return "dbt_done"


@op
def run_yolo_enrichment():
    result = subprocess.run(
        ["python", "src/yolo_detect.py"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise Failure(result.stderr)

    return "yolo_done"