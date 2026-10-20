# ProofPolicy — Evidence-Bound Policy Gate

A small standalone GenLayer Intelligent Contract concept for checking whether a submitted claim is supported by evidence and meets a stated policy.

## Why this primitive?

Many applications need more than a free-form AI answer. They need a bounded decision (`approve`, `reject`, or `inconclusive`), a reason, and an explicit reference to the evidence considered. ProofPolicy demonstrates that pattern in a reusable contract.

This is a starter submission package, not a claim that the contract has been deployed or accepted. Reviewers should run it in the current GenLayer Studio/runtime and adjust imports or entrypoint conventions if their selected SDK version differs.

## Consensus design

The `review_claim` method asks the GenLayer-supported language-model execution path to evaluate a claim against a policy and evidence text. The prompt requires a narrow JSON result with:
- `decision`: `approve`, `reject`, or `inconclusive`
- `reason`: concise explanation
- `evidence_quote`: a short verbatim quote from the supplied evidence, or an empty string

The contract validates the response shape and allowed decision values. It also checks that a non-empty evidence quote occurs in the submitted evidence. If parsing or validation fails, the result becomes `inconclusive` rather than silently accepting malformed output.

GenLayer consensus is useful here because validators can independently evaluate the same bounded task and compare structured outcomes under the runtime's consensus mechanism. Exact consensus behavior depends on the deployed GenLayer runtime and SDK version; this package does not claim a live consensus run has been completed.

## Contract state

The contract stores the latest review:
- `last_claim`
- `last_policy`
- `last_decision`
- `last_reason`
- `last_evidence_quote`
- `review_count`

A review is a decision-support primitive, not a substitute for legal, medical, financial, or other professional judgment.

## Files

- `contracts/proof_policy.py` — contract source
- `tests/test_validation.py` — local deterministic tests for response validation
- `examples/example_input.json` — sample claim, policy, and evidence
- `DEPLOYMENT.md` — practical deployment checklist
- `LICENSE` — MIT license

## Local tests

The validation helper tests use Python's standard library and do not require GenLayer packages:

```bash
python -m unittest discover -s tests -v
```

These tests cover local validation logic only. They do not execute GenVM, prove validator agreement, or confirm deployment.

## Example use

Input claim: `The product has a 30-day refund policy.`
Policy: `Approve only if the evidence explicitly states the refund period.`
Evidence: `Customers may request a refund within 30 days of purchase.`

Expected high-level result: `approve`, with a quote from the evidence. Actual model output and consensus outcome can vary by runtime and must be tested in GenLayer Studio.

## Before submitting

1. Open the current official GenLayer Studio and create a new Intelligent Contract.
2. Review the current SDK template and ensure the import/decorator/API conventions match.
3. Paste or upload `contracts/proof_policy.py`.
4. Run the example in Studio and inspect the execution result.
5. Run local tests with the command above.
6. Add screenshots or a transaction/execution reference only after a real successful run.
7. Do not describe the contract as deployed or tested in GenLayer unless you have verified it.

## Submission description

**ProofPolicy is a reusable evidence-bound policy gate.** It takes a claim, a policy, and evidence text, then returns a constrained decision with a reason and a quote that must appear in the evidence. It is designed to demonstrate how GenLayer consensus can support bounded, auditable decision workflows instead of unconstrained AI responses. The contract includes defensive output validation and falls back to `inconclusive` when the model response cannot be trusted.
