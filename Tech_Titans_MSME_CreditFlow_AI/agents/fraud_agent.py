class FraudInvestigationAgent:
    name = "Fraud Investigation Agent"
    KEYWORDS = ("round cash", "unknown beneficiary", "cash withdrawal", "reversal", "suspicious")
    def run(self, transaction_file):
        if transaction_file is None:
            return {"status":"REVIEW","flags":[],"flag_count":0,"note":"No transaction CSV supplied."}
        import pandas as pd
        df = pd.read_csv(transaction_file)
        if "description" not in df:
            return {"status":"REVIEW","flags":[],"flag_count":0,"note":"Description column missing."}
        flags = []
        for idx, desc in df["description"].fillna("").astype(str).items():
            hits = [k for k in self.KEYWORDS if k in desc.lower()]
            if hits:
                flags.append({"row":int(idx)+2,"description":desc,"matched_indicators":hits})
        return {"status":"FLAG" if flags else "PASS","flags":flags,"flag_count":len(flags),
                "note":"Keyword screening only; a flag is an investigation lead, not proof of fraud."}
