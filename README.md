# 🏛️ MPLADS Integrity Console

A focused command centre for transparent, accountable project implementation, built for the **Smart India Hackathon**.

---

## 🚀 Overview
The **MPLADS Integrity Console** is designed to monitor, score, and streamline constituency project data. It ensures transparency, tracks implementation metrics, and provides a clear workspace interface for evaluating project performance.

---

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **Frontend:** HTML5, CSS3, JavaScript (`app.js`)
* **Data Handling:** CSV-based structured data tracking (`mplads_scored_results-1.csv`)

---

## 🚀 Getting Started & Local Installation

Follow these steps to set up and run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/TanviG03/MPLADS-console.git](https://github.com/TanviG03/MPLADS-console.git)
cd MPLADS-console
python -m venv .venv
.venv\Scripts\Activate.ps1
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend:app --reload --port 8001
python -m http.server 5500
### Final step to update it on GitHub:
After saving the file cleanly in VS Code, update it live by running these commands in your terminal:
```powershell
git add README.md
git commit -m "Fix formatting and structure in README.md"
git push origin main
