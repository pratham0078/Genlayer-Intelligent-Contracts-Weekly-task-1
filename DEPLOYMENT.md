# Deployment checklist

This package has not been verified against a live GenLayer Studio deployment.

1. Open the current official GenLayer Studio / Playground.
2. Create a new Intelligent Contract using the current Python template.
3. Compare the generated template's imports, decorators, and LLM call API with `contracts/proof_policy.py`.
4. If the current template differs, adapt the contract to that exact SDK version before deploying. In particular, confirm `gl.exec_prompt`, `@gl.public.write`, and `@gl.public.view` are supported by the runtime you are using.
5. Deploy to the intended test network.
6. Call `review_claim` with the fields from `examples/example_input.json`.
7. Confirm the returned quote is an exact substring of the evidence and the decision is one of the allowed values.
8. Call `get_latest_review` and confirm the state reflects the most recent review.
9. Save the real execution reference and screenshots for your submission.

Do not claim successful deployment, runtime compatibility, or validator consensus until you have observed it in Studio.
