def create_proposal(case_id, applicant, structure, human_decision=None, officer_note=""):
    if human_decision not in ("APPROVE", "REJECT", "PENDING"):
        human_decision = "PENDING"
    return {
        "case_id": case_id,
        "account_name": applicant.get("business_name"),
        "proposed_amount": structure.get("proposed_amount", 0),
        "tenure_months": structure.get("tenure_months"),
        "status": "PROPOSAL_ONLY" if human_decision == "PENDING" else f"HUMAN_{human_decision}",
        "human_decision": human_decision,
        "officer_note": officer_note,
        "ledger_note": "Mock ledger entry only. No funds movement, account creation or disbursement."
    }
