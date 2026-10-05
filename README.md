# MPLADS AI Monitor

## Start the backend

From this folder, create or activate a Python environment and install the dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start FastAPI on port `8001`:

```powershell
uvicorn backend:app --reload --port 8001
```

The frontend is a static app. Serve it on another port so it can call the API:

```powershell
python -m http.server 5500
```

Open `http://localhost:5500/` in the browser.

## API endpoints

- `GET /api/mps` returns available MPs, project counts, and total records.
- `GET /api/mps/{mp_id}/projects` returns projects for one MP.
- `GET /api/projects/{project_id}` returns one complete project record.
- `GET /api/projects/{project_id}/analysis-data` returns the fields used by the prototype AI analysis.

The backend reads `mplads_scored_results-1.csv` from the same folder. It returns `404` for unknown MPs/projects and `503` when the CSV is missing or cannot be read. CORS is enabled for the local static frontend.

## Frontend connection

`app.js` calls the FastAPI API at `http://localhost:8001`. MP choices come from `/api/mps`; selecting an MP loads its projects from `/api/mps/{mp_id}/projects`. Project details use `/api/projects/{project_id}`, analysis uses `/analysis-data`, and the AI Assistant uses the selected MP project response as its context.
