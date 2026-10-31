class PolicyComplianceAgent:
    def run(self, applicant, risk, cashflow, fraud):
        requested = float(applicant.get("requested_amount") or 0)
        max_demo_limit = 500000
        checks = [
            {"rule":"Positive requested amount","passed":requested > 0,"detail":"Requested amount must be greater than zero."},
            {"rule":"Demo exposure cap","passed":requested <= max_demo_limit,"detail":f"Prototype cap is ₹{max_demo_limit:,.0f}."},
            {"rule":"No unresolved high-risk band","passed":risk.get("risk_band") != "HIGH","detail":"High-risk cases require rejection/escalation in this demo."},
            {"rule":"Fraud flags reviewed","passed":fraud.get("flag_count",0) == 0,"detail":"Any indicator requires manual investigation."},
            {"rule":"Cash-flow evidence present","passed":cashflow.get("status") != "REVIEW","detail":"Transaction data is required for this demo workflow."}
        ]
        failed = [c["rule"] for c in checks if not c["passed"]]
        return {"checks":checks,"failed_checks":failed,"status":"PASS" if not failed else "HOLD"}
