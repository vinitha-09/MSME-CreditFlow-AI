import io
from core.orchestrator import CreditFlowOrchestrator

def test_orchestrator_routes_case():
    applicant = {"applicant_name":"Test","business_name":"Test Co","loan_purpose":"Working capital",
                 "business_vintage":3,"requested_amount":10000,"tenure_months":12}
    csv = io.StringIO("date,description,type,amount\n2026-01-01,sale,credit,100000\n2026-01-02,cost,debit,10000\n")
    case = CreditFlowOrchestrator().run(applicant,csv,[])
    assert "credit_risk" in case.results
    assert "policy" in case.results
    assert len(case.messages) >= 8
