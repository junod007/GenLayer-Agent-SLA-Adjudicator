# Test 02 — Consensus Evaluation

## Test objective

Verify the complete GenLayer adjudication path:

`PENDING -> non-deterministic web evidence -> LLM evaluation -> Equivalence Principle -> consensus -> EVALUATED`

## Input

- SLA ID: `0`
- Evidence URL: `https://example.com`
- Expected outcome: `UNDETERMINED`

The placeholder page was selected intentionally because it does not contain proof that the requested service was completed.

## Consensus evidence

The Studio execution log showed:

- `Consensus ACCEPTED`
- `Reached consensus`
- `FINALIZED`

The Studio also completed the contract execution and returned an adjudication result.

## Final on-chain state

`get_sla(0)` returned:

- `status = EVALUATED`
- `decision = UNDETERMINED`
- `reason` populated with an explanation that the evidence page was insufficient to demonstrate completion of the requested service by the deadline.

## Why this test matters

The contract did not turn weak evidence into an `ACCEPTED` result. Instead, it committed `UNDETERMINED`, which is the intended conservative outcome when the evidence does not support a reliable decision.

## Evidence to attach

Add the Studio screenshots showing:

1. Consensus / execution log
2. Final `get_sla(0)` state

Suggested filenames:

- `02-consensus.png`
- `03-final-state.png`
