# MSME CreditFlow AI
## Project Report – Virtusa Jatayu Season 6

**Team Name:** Tech Titans  
**Use Case:** 1 – MSME Loan Underwriting Desk  
**Project Type:** Agentic AI Decision-Support Prototype

## 1. Abstract

MSME CreditFlow AI is a multi-agent decision-support prototype designed to assist financial institutions in evaluating MSME loan applications. It coordinates specialized agents to analyze applicant information, transaction data, cash flow, potential fraud indicators, credit risk and lending policy requirements.

The system generates a Credit Appraisal Memo (CAM) containing findings and a proposed loan structure. A human reviewer makes the final decision.

## 2. Introduction

Micro, Small and Medium Enterprises (MSMEs) often face delays in loan underwriting because financial institutions must review multiple documents and assess repayment capacity, financial risks and policy requirements.

MSME CreditFlow AI aims to organize this process through a coordinated multi-agent workflow.

## 3. Problem Statement

Manual MSME loan underwriting can be time-consuming and inconsistent. Officers need to examine financial transactions, identify unusual activities, assess repayment capacity and verify lending policy conditions.

The proposed prototype helps organize these activities and provides evidence-based findings for human review.

## 4. Objectives

- Automate parts of the loan assessment workflow.
- Analyze transaction and cash-flow information.
- Identify potential fraud indicators.
- Assess credit risk using transparent rules.
- Validate configurable lending policies.
- Generate a Credit Appraisal Memo.
- Maintain case history and human decisions.

## 5. Proposed System

The proposed system uses specialist software agents coordinated by a central orchestrator. Agents share their findings through a shared case file and structured messages.

## 6. Technologies Used

- Python
- Streamlit
- Pandas
- SQLite (if enabled in the implementation)
- Pytest
- Visual Studio Code

## 7. System Workflow

1. Applicant and loan details are entered.
2. Supporting evidence files are uploaded.
3. Document intake agent records available evidence.
4. Cash-flow agent analyzes transaction data.
5. Fraud investigation agent identifies suspicious indicators.
6. Credit risk agent evaluates risk.
7. Policy agent checks configured lending rules.
8. Loan structuring agent proposes loan terms.
9. The system generates the CAM.
10. A human reviewer approves, rejects or holds the case.

## 8. Implementation

The application provides a Streamlit interface for creating underwriting cases, analyzing transaction CSV files, viewing agent findings, generating CAM reports and reviewing saved cases.

## 9. Testing

Automated tests are executed using:

`python -m pytest tests -v`

Record the actual test results and manual testing evidence in the separate test report.

## 10. Limitations

- The prototype uses synthetic or demonstration data.
- It does not connect to live banking, GST, Udyam or credit bureau services.
- Supporting document uploads do not necessarily mean their contents are automatically extracted.
- Fraud and risk findings depend on configured rules and available data.
- The prototype is not a production lending platform.

## 11. Future Enhancements

- Integrate OCR for extracting information from financial documents.
- Connect verified external financial data services.
- Improve fraud detection using transaction graph analysis.
- Add configurable AI/LLM support.
- Introduce stronger authentication and role-based access.
- Expand automated and integration testing.

## 12. Conclusion

MSME CreditFlow AI demonstrates how a coordinated multi-agent workflow can support MSME loan underwriting. It organizes financial analysis, risk assessment, policy validation and CAM generation while retaining mandatory human decision-making.

**Final loan approval and disbursement are outside the autonomous scope of this prototype.**