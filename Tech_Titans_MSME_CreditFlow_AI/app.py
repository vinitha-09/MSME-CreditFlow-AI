import streamlit as st
import pandas as pd
from pathlib import Path
from core.orchestrator import CreditFlowOrchestrator
from services.cam_generator import generate_cam
from services.mock_ledger import create_proposal
from database.db import init_db, save_case, list_cases, get_audit, record_decision

st.set_page_config(page_title="MSME CreditFlow AI | Tech Titans", page_icon="🏦", layout="wide")
init_db()

st.title("🏦 MSME CreditFlow AI")
st.caption("Agentic decision-support prototype | Team Tech Titans | Use Case 1")
st.warning("Demo only: synthetic data + deterministic rules. No real bank integrations, automatic sanction, or disbursement.")
tab1, tab2, tab3 = st.tabs(["New underwriting case", "Case history & human approval", "About & architecture"])

with tab1:
    st.subheader("1. Applicant and loan details")
    c1,c2 = st.columns(2)
    with c1:
        applicant_name = st.text_input("Applicant name", "Aarav Kumar")
        business_name = st.text_input("Business name", "Sri Lakshmi Engineering Works")
        loan_purpose = st.selectbox("Loan purpose", ["Working capital","Machinery purchase","Business expansion","Inventory"])
        business_vintage = st.number_input("Business vintage (years)", min_value=0, max_value=100, value=4)
    with c2:
        requested_amount = st.number_input("Requested loan amount (₹)", min_value=0, value=300000, step=10000)
        tenure_months = st.selectbox("Requested tenure (months)", [12,18,24,36,48,60], index=2)
        annual_turnover = st.number_input("Declared annual turnover (₹)", min_value=0, value=1800000, step=50000)
        gstin = st.text_input("GSTIN / Udyam reference (demo text only)", "DEMO-GST-0001")
    st.subheader("2. Evidence files")
    transaction_file = st.file_uploader("Upload transaction CSV", type=["csv"])
    other_docs = st.file_uploader("Upload supporting files (PDF/TXT/CSV; filename capture only)", type=["pdf","txt","csv"], accept_multiple_files=True)
    st.caption("CSV format: date, description, type, amount. See data/sample_transactions.csv.")
    run = st.button("Run multi-agent underwriting", type="primary", use_container_width=True)
    if run:
        applicant = {"applicant_name":applicant_name,"business_name":business_name,"loan_purpose":loan_purpose,
                     "business_vintage":business_vintage,"requested_amount":requested_amount,
                     "tenure_months":tenure_months,"annual_turnover":annual_turnover,"gstin":gstin}
        try:
            case = CreditFlowOrchestrator().run(applicant, transaction_file, [f.name for f in other_docs])
            cam = generate_cam(case)
            st.session_state["active_case"] = case
            st.session_state["active_cam"] = cam
            save_case(case,cam)
            st.success(f"Analysis complete. Case ID: {case.case_id}")
        except Exception as e:
            st.error(f"Could not complete analysis: {e}")

    if "active_case" in st.session_state:
        case = st.session_state["active_case"]
        res = case.results
        st.divider()
        st.subheader("3. Underwriting results")
        a,b,c,d = st.columns(4)
        a.metric("Risk score", f"{res['credit_risk']['score']}/100")
        b.metric("Risk band", res["credit_risk"]["risk_band"])
        c.metric("Policy", res["policy"]["status"])
        d.metric("Fraud indicators", res["fraud"]["flag_count"])
        for key,title in [("document_intake","Document intake"),("cashflow","Cash-flow analysis"),("fraud","Fraud investigation"),("credit_risk","Credit risk"),("policy","Policy & compliance"),("loan_structuring","Loan structuring")]:
            with st.expander(title, expanded=(key in ["credit_risk","policy"])):
                st.json(res[key])
        st.subheader("4. Proposed loan terms")
        st.json(res["loan_structuring"])
        st.download_button("Download Credit Appraisal Memo (.md)", st.session_state["active_cam"],
                           file_name=f"{case.case_id}_CAM.md", mime="text/markdown")
        st.download_button("Download agent message log (.json)", __import__("json").dumps(case.messages,indent=2),
                           file_name=f"{case.case_id}_agent_messages.json", mime="application/json")

with tab2:
    st.subheader("Saved cases")
    cases = list_cases()
    if cases:
        st.dataframe(pd.DataFrame(cases)[["case_id","created_at","business_name","requested_amount","risk_band","policy_status","human_decision"]], use_container_width=True)
        selected = st.selectbox("Select case for human review", [x["case_id"] for x in cases])
        selected_case = next(x for x in cases if x["case_id"] == selected)
        st.write("**Business:**", selected_case["business_name"], "| **Risk:**", selected_case["risk_band"], "| **Policy:**", selected_case["policy_status"])
        st.text_area("CAM preview", selected_case["cam_text"], height=240)
        st.markdown("**Human officer decision**")
        decision = st.radio("Decision", ["PENDING","APPROVE","REJECT"], horizontal=True, key="decision_"+selected)
        note = st.text_area("Officer review note", key="note_"+selected)
        if st.button("Record human decision", type="primary"):
            record_decision(selected,decision,note)
            st.success("Human decision recorded in SQLite audit trail.")
        ledger = create_proposal(selected, {"business_name":selected_case["business_name"]},
                                 {"proposed_amount":selected_case["requested_amount"]}, decision, note)
        st.markdown("**Mock ledger preview**")
        st.json(ledger)
        st.caption("The mock ledger stores a proposal/decision status only. It never transfers funds.")
        with st.expander("Audit trail"):
            st.dataframe(pd.DataFrame(get_audit(selected)), use_container_width=True)
    else:
        st.info("No cases saved yet. Run a new underwriting case first.")

with tab3:
    st.subheader("Solution overview")
    st.write("A multi-agent workflow coordinates specialist checks through a shared case file and structured messages.")
    st.graphviz_chart("""digraph G {
      rankdir=LR; node [shape=box, style=rounded];
      Intake -> Cashflow -> Fraud -> Risk -> Policy -> Structuring -> CAM -> "Mock Ledger" -> "Human Approval";
      Orchestrator -> Intake; Orchestrator -> Risk; Orchestrator -> Policy;
    }""")
    st.markdown("""
**Agents**
- Document Intake: checks required application fields and records uploaded filenames.
- Cash-Flow: calculates inflows, outflows and net cash flow from CSV.
- Fraud Investigation: flags configured transaction-description indicators for review.
- Credit Risk: produces a transparent demo score and risk band.
- Policy & Compliance: enforces hard-coded demonstration rules.
- Loan Structuring: calculates an illustrative EMI only when policy checks pass.

**Safety and limitations**
- No real credit decision, credit-bureau score, GST/KYC/ITR verification or external banking API.
- Uploaded supporting documents are not OCR-extracted; only filenames are recorded.
- Fraud keyword hits are leads, not proof.
- All proposed terms require an authorized human decision.
- No automatic sanction, account opening or disbursement.
""")
