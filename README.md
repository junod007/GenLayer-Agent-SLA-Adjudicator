# GenLayer Agent SLA Adjudicator

An on-chain SLA adjudication primitive for AI agents that evaluates externally verifiable service evidence and commits a consensus-backed fulfillment decision.

## Why this contract exists

AI-agent commerce needs a neutral way to decide whether an agent actually fulfilled an agreed service. A deterministic smart contract cannot reliably judge evidence expressed in natural language or retrieved from public web sources.

This Intelligent Contract stores the SLA terms on-chain, retrieves the specified evidence through GenLayer's non-deterministic web access, evaluates the evidence with an LLM, and uses the Equivalence Principle to require validators to agree on the important decision field.

## Core flow

1. A client creates an SLA.
2. The contract stores:
   - client
   - agent
   - service requirement
   - evidence URL
   - deadline
   - evaluation criteria
3. The contract starts in `PENDING`.
4. `evaluate_sla()` retrieves the evidence and asks an impartial adjudicator to classify it.
5. GenLayer validators independently verify the non-deterministic result.
6. The contract commits:
   - `ACCEPTED`
   - `REJECTED`
   - or `UNDETERMINED`
7. The factual reason is stored on-chain with the decision.

## Decision policy

| Decision | Meaning |
|---|---|
| `ACCEPTED` | Evidence clearly demonstrates that the SLA requirements were fulfilled. |
| `REJECTED` | Evidence clearly demonstrates that the requirements were not fulfilled. |
| `UNDETERMINED` | Evidence is missing, insufficient, contradictory, or does not allow a reliable determination. |

The contract explicitly avoids inventing facts when evidence is weak.

## GenLayer-specific logic

This is intentionally not a generic Solidity-style contract.

### Web evidence

`gl.nondet.web.get()` retrieves the evidence page during non-deterministic execution.

### LLM adjudication

`gl.nondet.exec_prompt(..., response_format="json")` converts the evidence and SLA criteria into a structured decision.

### Equivalence Principle

`gl.eq_principle.prompt_comparative()` requires the important `decision` field to match across validator executions. The reason must remain factually consistent with that decision.

### State transition

`PENDING -> EVALUATED`

The final decision and reason are committed to contract storage.

## Testnet deployment

- Network: GenLayer Studionet / GenLayer Studio
- Contract: `AgentSLAAdjudicator`
- Deployed contract address: `0xc649D065d7b70B801E3c2F46Ae2f1933F2fAFC32`
- Test SLA ID: `0`
- Client / test agent: `0xA128a89295926939B3CB161e8990E74f4D365093`

## Verified test

The first integration test intentionally used a weak evidence source:

- Evidence URL: `https://example.com`
- SLA status before evaluation: `PENDING`
- Decision before evaluation: `UNDETERMINED`
- Evaluation: finalized after GenLayer consensus
- Final SLA status: `EVALUATED`
- Final decision: `UNDETERMINED`
- Final reason: the supplied page did not provide sufficient evidence that the requested service was completed by the deadline.

This is a deliberate negative/insufficient-evidence test. It demonstrates that the contract can refuse to make an unsupported positive determination.

## Files

- `agent_sla_adjudicator.py` — Intelligent Contract source
- `evidence/test-01-create-sla.md` — creation and pending-state evidence
- `evidence/test-02-consensus-evaluation.md` — consensus evaluation and final-state evidence

## Limitations

This test uses a public placeholder webpage as intentionally insufficient evidence. It proves the adjudication path and the `UNDETERMINED` safety outcome, but it is not a positive proof of SLA fulfillment.

For production use, evidence sources should be stable, structured, attributable, and designed to remain independently verifiable.

## Future extensions

- Multiple evidence URLs
- Evidence timestamps and provenance
- Appeal / re-review flow
- Payment release after `ACCEPTED`
- Agent reputation updates after adjudication
- Explicit deadline validation
