# Test plan and expected demo checks

| Test | Action | Expected result |
|---|---|---|
| Valid CSV | Upload sample_transactions.csv | Credits/debits/net cash flow are calculated |
| Fraud indicator | Use description containing 'unknown beneficiary' | A review flag appears |
| Missing CSV | Run without transaction CSV | Cash-flow status is REVIEW; policy holds |
| Negative cash flow | Upload CSV where debits exceed credits | Cash-flow FLAG and lower risk score |
| Policy cap | Request more than ₹5,00,000 | Policy HOLD |
| Human review | Record APPROVE or REJECT in case history | SQLite case and audit trail update |

Automated tests cover core cash-flow arithmetic and orchestrator output. The remaining checks are manual UI acceptance tests.
