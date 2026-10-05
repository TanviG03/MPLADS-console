from csv import DictReader
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "mplads_scored_results-1.csv"

app = FastAPI(title="MPLADS AI Monitor API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def load_projects() -> list[dict[str, Any]]:
    if not CSV_PATH.exists():
        raise HTTPException(status_code=503, detail="MPLADS CSV dataset is unavailable")
    try:
        with CSV_PATH.open(newline="", encoding="utf-8-sig") as csv_file:
            return list(DictReader(csv_file))
    except OSError as error:
        raise HTTPException(status_code=503, detail="MPLADS CSV dataset could not be read") from error


def project_or_404(project_id: str) -> dict[str, Any]:
    project = next((row for row in load_projects() if row.get("work_id") == project_id), None)
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' was not found")
    return project


@app.get("/api/mps")
def get_mps() -> dict[str, Any]:
    projects = load_projects()
    grouped: dict[str, int] = {}
    for project in projects:
        mp_id = project.get("mp", "")
        grouped[mp_id] = grouped.get(mp_id, 0) + 1
    return {
        "total_records": len(projects),
        "mps": [
            {"mp_id": mp_id, "project_count": count}
            for mp_id, count in sorted(grouped.items(), key=lambda item: int(item[0].split("_")[-1]))
        ],
    }


@app.get("/api/mps/{mp_id}/projects")
def get_mp_projects(mp_id: str) -> dict[str, Any]:
    projects = [project for project in load_projects() if project.get("mp") == mp_id]
    if not projects:
        raise HTTPException(status_code=404, detail=f"MP '{mp_id}' was not found")
    return {"mp_id": mp_id, "count": len(projects), "projects": projects}


@app.get("/api/projects/{project_id}")
def get_project(project_id: str) -> dict[str, Any]:
    return project_or_404(project_id)


@app.get("/api/projects/{project_id}/analysis-data")
def get_analysis_data(project_id: str) -> dict[str, Any]:
    project = project_or_404(project_id)
    fields = [
        "work_id", "mp", "district", "category", "sanctioned_amount", "expenditure",
        "sanction_days_ago", "completion_days", "cost_deviation_ratio",
        "expenditure_overrun_ratio", "is_anomaly", "is_vendor_ring",
        "vendor_network_flag",
    ]
    return {field: project.get(field, "") for field in fields}
