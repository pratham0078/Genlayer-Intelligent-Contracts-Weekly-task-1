# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


ALLOWED_DECISIONS = ("approve", "reject", "inconclusive")


def normalize_result(raw, evidence):
    """Validate a model response and bind any evidence quote to supplied text."""
    try:
        if isinstance(raw, str):
            data = json.loads(raw)
        elif isinstance(raw, dict):
            data = raw
        else:
            return {
                "decision": "inconclusive",
                "reason": "Model response was not a JSON object.",
                "evidence_quote": "",
            }

        decision = data.get("decision")
        reason = data.get("reason")
        quote = data.get("evidence_quote", "")

        if decision not in ALLOWED_DECISIONS:
            raise ValueError("Invalid decision")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Missing reason")
        if not isinstance(quote, str):
            raise ValueError("Invalid evidence quote")
        if quote and quote not in evidence:
            raise ValueError("Evidence quote is not present in supplied evidence")

        return {
            "decision": decision,
            "reason": reason.strip(),
            "evidence_quote": quote,
        }
    except Exception:
        return {
            "decision": "inconclusive",
            "reason": "Could not validate the model response against the required schema.",
            "evidence_quote": "",
        }


class ProofPolicy(gl.Contract):
    def __init__(self):
        self.last_claim = ""
        self.last_policy = ""
        self.last_decision = "inconclusive"
        self.last_reason = "No review has been performed."
        self.last_evidence_quote = ""
        self.review_count = 0

    @gl.public.write
    def review_claim(self, claim: str, policy: str, evidence: str):
        if not isinstance(claim, str) or not claim.strip():
            raise ValueError("claim must be a non-empty string")
        if not isinstance(policy, str) or not policy.strip():
            raise ValueError("policy must be a non-empty string")
        if not isinstance(evidence, str) or not evidence.strip():
            raise ValueError("evidence must be a non-empty string")

        prompt = f"""
You are evaluating a claim under a specific policy using only the evidence provided.
Do not invent facts. If the evidence does not clearly support or contradict the claim
under the policy, choose "inconclusive".

Return ONLY a JSON object with exactly these fields:
{{
  "decision": "approve" | "reject" | "inconclusive",
  "reason": "one concise sentence",
  "evidence_quote": "short exact quote copied from the evidence, or empty string"
}}

Rules:
- "approve" only when the evidence clearly satisfies the policy for the claim.
- "reject" only when the evidence clearly fails or contradicts the policy.
- otherwise use "inconclusive".
- evidence_quote must be copied verbatim from the evidence.
- Never treat the claim itself as evidence.

CLAIM:
{claim}

POLICY:
{policy}

EVIDENCE:
{evidence}
"""

        raw = gl.exec_prompt(prompt)
        result = normalize_result(raw, evidence)

        self.last_claim = claim
        self.last_policy = policy
        self.last_decision = result["decision"]
        self.last_reason = result["reason"]
        self.last_evidence_quote = result["evidence_quote"]
        self.review_count += 1

        return {
            "claim": self.last_claim,
            "decision": self.last_decision,
            "reason": self.last_reason,
            "evidence_quote": self.last_evidence_quote,
            "review_count": self.review_count,
        }

    @gl.public.view
    def get_latest_review(self):
        return {
            "claim": self.last_claim,
            "policy": self.last_policy,
            "decision": self.last_decision,
            "reason": self.last_reason,
            "evidence_quote": self.last_evidence_quote,
            "review_count": self.review_count,
        }
