import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parents[1] / ".creditflow" / "creditflow.db"

def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with connect() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY, created_at TEXT, applicant_name TEXT,
            business_name TEXT, requested_amount REAL, risk_band TEXT,
            policy_status TEXT, human_decision TEXT, cam_text TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT, case_id TEXT, timestamp TEXT,
            actor TEXT, action TEXT, details TEXT)""")

def save_case(case, cam_text, decision="PENDING"):
    import json
    r = case.results
    with connect() as con:
        con.execute("""INSERT OR REPLACE INTO cases VALUES (?,?,?,?,?,?,?,?,?)""", (
            case.case_id, case.created_at, case.applicant.get("applicant_name"),
            case.applicant.get("business_name"), float(case.applicant.get("requested_amount") or 0),
            r.get("credit_risk",{}).get("risk_band"), r.get("policy",{}).get("status"),
            decision, cam_text))
        for msg in case.messages:
            con.execute("INSERT INTO audit_log(case_id,timestamp,actor,action,details) VALUES (?,?,?,?,?)",
                (case.case_id,msg["timestamp"],msg["sender"],msg["type"],json.dumps(msg["payload"])))
        con.execute("INSERT INTO audit_log(case_id,timestamp,actor,action,details) VALUES (?,?,?,?,?)",
            (case.case_id,case.created_at,"System","CASE_SAVED","Case and CAM saved to SQLite"))

def record_decision(case_id, decision, note):
    from datetime import datetime
    with connect() as con:
        con.execute("UPDATE cases SET human_decision=? WHERE case_id=?", (decision,case_id))
        con.execute("INSERT INTO audit_log(case_id,timestamp,actor,action,details) VALUES (?,?,?,?,?)",
            (case_id,datetime.now().isoformat(timespec="seconds"),"Human Officer","DECISION_RECORDED",note))

def list_cases():
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()]

def get_audit(case_id):
    with connect() as con:
        return [dict(r) for r in con.execute("SELECT * FROM audit_log WHERE case_id=? ORDER BY id", (case_id,)).fetchall()]
