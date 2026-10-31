class LoanStructuringAgent:
    def run(self, applicant, risk, policy):
        amount = float(applicant.get("requested_amount") or 0)
        if policy.get("status") != "PASS":
            return {"status":"NOT_PROPOSED","proposed_amount":0,"tenure_months":None,
                    "monthly_installment":None,"note":"Terms not proposed because policy checks are on hold."}
        tenure = int(applicant.get("tenure_months") or 24)
        annual_rate = 12.0
        r = annual_rate / 1200
        emi = amount / tenure if r == 0 else amount*r*(1+r)**tenure/((1+r)**tenure-1)
        return {"status":"DRAFT","proposed_amount":amount,"annual_interest_rate_percent":annual_rate,
                "tenure_months":tenure,"monthly_installment":round(emi,2),
                "note":"Illustrative terms only; final pricing and sanction require authorized human review."}
