# Test 01 — Create SLA

## Test objective

Verify that an SLA can be created and that its initial state is stored correctly.

## Deployment

- Contract: `AgentSLAAdjudicator`
- Address: `0xc649D065d7b70B801E3c2F46Ae2f1933F2fAFC32`
- Network: GenLayer Studionet / GenLayer Studio
- Test wallet: `0xA128a89295926939B3CB161e8990E74f4D365093`

## Input

- SLA ID: `0`
- Agent: `0xA128a89295926939B3CB161e8990E74f4D365093`
- Evidence URL: `https://example.com`
- Service: AI agent market-report service
- Deadline: test deadline configured in Studio
- Criteria: evidence must clearly demonstrate that the requested service was completed by the deadline

## Observed state

After `create_sla()`:

- `status = PENDING`
- `decision = UNDETERMINED`
- `reason = ""`

This establishes the expected pre-adjudication state.

## Evidence to attach

Add the Studio screenshot showing the successful `create_sla()` execution and/or the `get_sla(0)` result.

Suggested filename:

`01-create-sla.png`
