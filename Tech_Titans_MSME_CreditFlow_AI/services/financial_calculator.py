import pandas as pd

def analyze_transactions(csv_path_or_buffer):
    df = pd.read_csv(csv_path_or_buffer)
    required = {"date", "description", "type", "amount"}
    if not required.issubset(set(df.columns)):
        raise ValueError(f"CSV must contain columns: {', '.join(sorted(required))}")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["type"] = df["type"].astype(str).str.lower().str.strip()
    credits = df.loc[df.type.isin(["credit", "inflow"]), "amount"].sum()
    debits = df.loc[df.type.isin(["debit", "outflow"]), "amount"].sum()
    months = max(1, df["date"].nunique() // 20 or 1)
    return {
        "transaction_count": int(len(df)),
        "total_credits": round(float(credits), 2),
        "total_debits": round(float(debits), 2),
        "net_cash_flow": round(float(credits-debits), 2),
        "avg_monthly_credits": round(float(credits/months), 2),
        "avg_monthly_debits": round(float(debits/months), 2),
        "months_estimated": int(months),
        "negative_net_cashflow": bool(credits-debits < 0)
    }
