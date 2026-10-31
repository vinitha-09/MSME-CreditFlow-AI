
import io

from agents.document_agent import DocumentAgent
from agents.cashflow_agent import CashFlowAgent
from agents.fraud_agent import FraudInvestigationAgent
from agents.credit_risk_agent import CreditRiskAgent
from agents.policy_agent import PolicyComplianceAgent
from agents.loan_structuring_agent import LoanStructuringAgent

from core.shared_case import SharedCase


class CreditFlowOrchestrator:
    """
    Coordinates specialist agents and routes findings
    through a shared case file.
    """

    def run(self, applicant, transaction_file, uploaded_names=None):

        # Prepare independent input streams for cash-flow and fraud agents.
        cashflow_input = None
        fraud_input = None

        if transaction_file is not None:

            # Read uploaded file content.
            if hasattr(transaction_file, "getvalue"):
                raw_csv = transaction_file.getvalue()

            elif hasattr(transaction_file, "read"):
                raw_csv = transaction_file.read()

            else:
                raw_csv = transaction_file

            # Convert bytes into text if necessary.
            if isinstance(raw_csv, bytes):
                csv_text = raw_csv.decode("utf-8-sig")
            else:
                csv_text = str(raw_csv)

            # Each agent receives a fresh stream.
            cashflow_input = io.StringIO(csv_text)
            fraud_input = io.StringIO(csv_text)

        # Create shared case file.
        case = SharedCase(applicant=applicant)

        # Step 1: Document, cash-flow and fraud agents.
        agents = [
            (
                "document_intake",
                DocumentAgent(),
                lambda agent: agent.run(applicant, uploaded_names)
            ),
            (
                "cashflow",
                CashFlowAgent(),
                lambda agent: agent.run(cashflow_input)
            ),
            (
                "fraud",
                FraudInvestigationAgent(),
                lambda agent: agent.run(fraud_input)
            ),
        ]

        # Execute each agent and record its findings.
        for key, agent, execute in agents:

            result = execute(agent)

            case.add_result(key, result)

            case.send(
                "Orchestrator",
                agent.name,
                "TASK",
                {"case_id": case.case_id}
            )

            case.send(
                agent.name,
                "Orchestrator",
                "FINDING",
                result
            )

        # Step 2: Credit risk assessment.
        risk = CreditRiskAgent().run(
            applicant,
            case.results["cashflow"],
            case.results["fraud"]
        )

        case.add_result("credit_risk", risk)

        case.send(
            "Credit Risk Agent",
            "Policy & Compliance Agent",
            "RISK_FINDING",
            risk
        )

        # Step 3: Policy and compliance validation.
        policy = PolicyComplianceAgent().run(
            applicant,
            risk,
            case.results["cashflow"],
            case.results["fraud"]
        )

        case.add_result("policy", policy)

        case.send(
            "Policy & Compliance Agent",
            "Loan Structuring Agent",
            "POLICY_RESULT",
            policy
        )

        # Step 4: Loan structuring.
        structure = LoanStructuringAgent().run(
            applicant,
            risk,
            policy
        )

        case.add_result("loan_structuring", structure)

        case.send(
            "Loan Structuring Agent",
            "Orchestrator",
            "PROPOSAL",
            structure
        )

        # Return the completed case for CAM generation and review.
        return case

