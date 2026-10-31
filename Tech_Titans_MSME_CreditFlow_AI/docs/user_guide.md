# User guide

1. Install Python 3.10 or newer and VS Code on Windows 11.
2. Extract the ZIP to a folder such as `C:\\Tech_Titans_MSME_CreditFlow_AI`.
3. Open that folder in VS Code.
4. Open Terminal → New Terminal.
5. Create a virtual environment: `py -m venv .venv`
6. Activate it in PowerShell: `.venv\\Scripts\\Activate.ps1`
   - If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.
   - Or use Command Prompt: `.venv\\Scripts\\activate.bat`
7. Install packages: `python -m pip install -r requirements.txt`
8. Start app: `python -m streamlit run app.py`
9. Browser opens at `http://localhost:8501`.
10. Enter sample applicant details, upload `data/sample_transactions.csv`, then click Run multi-agent underwriting.
11. Review each agent result and download the CAM.
12. Open Case history & human approval to record a human decision and inspect audit events.

## CSV format
Required columns: `date`, `description`, `type`, `amount`. `type` should be `credit` or `debit`. Use synthetic/demo records only.

## Run tests
`python -m pip install pytest`
`python -m pytest -q`
