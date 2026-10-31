class CreditRiskAgent:
    def run(self, applicant, cashflow, fraud):
        score = 100
        reasons = []
        if cashflow.get("status") == "REVIEW":
            score -= 15; reasons.append("Cash-flow data unavailable or incomplete")
        elif cashflow.get("negative_net_cashflow"):
            score -= 30; reasons.append("Net cash flow is negative")
        if fraud.get("flag_count", 0):
            score -= min(30, fraud["flag_count"] * 10); reasons.append("Potential transaction indicators require investigation")
        amount = float(applicant.get("requested_amount") or 0)
        if amount <= 0:
            score -= 20; reasons.append("Requested amount is invalid")
        if not applicant.get("business_vintage"):
            score -= 5; reasons.append("Business vintage not supplied")
        score = max(0, min(100, score))
        band = "LOW" if score >= 75 else ("MEDIUM" if score >= 50 else "HIGH")
        return {"score":score,"risk_band":band,"reasons":reasons,
                "status":"PASS" if band == "LOW" else "REVIEW",
                "note":"Transparent demonstration score; not a validated lending or bureau score."}
