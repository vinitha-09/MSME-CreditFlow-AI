# MSME CreditFlow AI — Team Tech Titans

A Windows-friendly, no-paid-API prototype for Virtusa Jatayu Use Case 1: MSME Loan Underwriting Desk.

## What it demonstrates
- Six specialist agents coordinated by an orchestrator.
- Shared case file / blackboard and structured A2A-style messages.
- CSV cash-flow analysis and transparent fraud indicator screening.
- Explainable demo risk score and deterministic policy checks.
- Illustrative loan EMI, evidence-oriented CAM and downloadable message log.
- SQLite case storage and audit trail.
- Mock ledger and mandatory human decision.

## Quick start (Windows 11)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
Open `http://localhost:8501` if it does not open automatically. Full instructions: `docs/user_guide.md`.

## Demo data
Upload `data/sample_transactions.csv`. Required CSV columns: `date, description, type, amount`.

## Project layout
- `app.py` — Streamlit application
- `agents/` — six specialist agents
- `core/` — shared case, message contract and orchestrator
- `services/` — calculations, CAM and mock ledger
- `database/` — SQLite persistence and audit log
- `data/` — synthetic example data
- `docs/` — architecture, workflow, user guide and test plan
- `tests/` — automated tests

## Important limitations
This is an educational proof of concept, not a production lending system. It uses synthetic data and deterministic rules. Supporting PDF/TXT/CSV files are currently captured by filename only; there is no OCR or document authenticity verification. There are no live integrations to banks, GST, ITR, KYC, Udyam or credit bureaus. Risk scoring is illustrative, not validated. Fraud indicators are not proof of wrongdoing. No automated sanction, account opening or disbursement occurs. A human officer must make the final decision.

## Team
Team name: Tech Titans | Team size: 4
