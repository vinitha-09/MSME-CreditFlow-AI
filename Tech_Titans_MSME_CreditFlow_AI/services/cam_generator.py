from datetime import datetime

def generate_cam(case):
    a = case.applicant
    r = case.results
    risk = r.get("credit_risk", {})
    policy = r.get("policy", {})
    struct = r.get("loan_structuring", {})
    lines = [
        "# CREDIT APPRAISAL MEMO (CAM)",
        f"Case ID: {case.case_id}",
        f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')}",
        "",
        "## 1. Applicant",
        f"- Applicant: {a.get('applicant_name','Not supplied')}",
        f"- Business: {a.get('business_name','Not supplied')}",
        f"- Loan purpose: {a.get('loan_purpose','Not supplied')}",
        f"- Requested amount: ₹{float(a.get('requested_amount') or 0):,.2f}",
        "",
        "## 2. Agent findings",
    ]
    for key, title in [("document_intake","Document intake"),("cashflow","Cash-flow"),("fraud","Fraud investigation"),("credit_risk","Credit risk"),("policy","Policy & compliance"),("loan_structuring","Loan structuring")]:
        lines += [f"### {title}", "```json", __import__("json").dumps(r.get(key,{}), indent=2, ensure_ascii=False), "```", ""]
    lines += [
        "## 3. Recommendation status",
        f"- Risk band: {risk.get('risk_band','Not assessed')}",
        f"- Policy status: {policy.get('status','Not assessed')}",
        f"- Proposed terms status: {struct.get('status','Not proposed')}",
        "",
        "## 4. Human decision",
        "This is a decision-support prototype. An authorized credit officer must review source evidence, resolve flags, approve/reject the proposal and record the decision. No automatic sanction or disbursement is performed.",
        "",
        "## 5. Limitations",
        "Synthetic/demo inputs and transparent rules are used. No live bank, GST, ITR, KYC, Udyam or bureau verification is connected. This memo is not a real credit decision."
    ]
    return "\\n".join(lines)
