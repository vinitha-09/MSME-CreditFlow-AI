import io
from services.financial_calculator import analyze_transactions

def test_cashflow_totals():
    csv = io.StringIO("date,description,type,amount\n2026-01-01,sale,credit,100\n2026-01-02,cost,debit,40\n")
    result = analyze_transactions(csv)
    assert result["total_credits"] == 100
    assert result["total_debits"] == 40
    assert result["net_cash_flow"] == 60
