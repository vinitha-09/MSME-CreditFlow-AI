# Architecture

## Design
The prototype uses a modular, orchestrated multi-agent pattern. `CreditFlowOrchestrator` creates a `SharedCase`, invokes specialist agents, stores their findings and records structured messages. The shared case acts as a blackboard. Agent outputs are dictionaries so they can be serialized to JSON and audited.

## Components
- Streamlit UI: applicant intake, CSV upload, results, CAM download and human review.
- Orchestrator: deterministic workflow coordination.
- Specialist agents: document intake, cash-flow, fraud screening, risk, policy and loan structuring.
- Services: financial calculations, CAM generation and mock ledger proposal.
- SQLite: cases and audit events.
- Data: synthetic CSV only.

## Message flow
1. Orchestrator → Document Intake: TASK
2. Document Intake → Orchestrator: FINDING
3. Orchestrator → Cash-Flow and Fraud agents: TASK/FINDING
4. Cash-Flow and Fraud findings → Credit Risk agent
5. Credit Risk → Policy agent: RISK_FINDING
6. Policy → Loan Structuring: POLICY_RESULT
7. Loan Structuring → Orchestrator: PROPOSAL
8. CAM and message log are generated; human officer reviews the case.

This is an A2A-style internal message contract, not a claim of implementing a third-party A2A protocol or distributed agent runtime.
