from services.financial_calculator import analyze_transactions

class CashFlowAgent:
    name = "Cash-Flow Analysis Agent"
    def run(self, transaction_file):
        if transaction_file is None:
            return {"status":"REVIEW","note":"No transaction CSV supplied.","net_cash_flow":None}
        result = analyze_transactions(transaction_file)
        result["status"] = "FLAG" if result["negative_net_cashflow"] else "PASS"
        result["note"] = "Computed from supplied transaction CSV; figures are indicative and not independently verified."
        return result
