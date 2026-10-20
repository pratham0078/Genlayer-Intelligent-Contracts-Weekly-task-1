import importlib.util
import pathlib
import unittest

CONTRACT_PATH = pathlib.Path(__file__).resolve().parents[1] / "contracts" / "proof_policy.py"

# Load only the pure helper function without importing GenLayer's runtime module.
SOURCE = CONTRACT_PATH.read_text(encoding="utf-8")
START = SOURCE.index("def normalize_result(")
END = SOURCE.index("\n\nclass ProofPolicy", START)
HELPER_SOURCE = SOURCE[START:END]
NAMESPACE = {"json": __import__("json"), "ALLOWED_DECISIONS": ("approve", "reject", "inconclusive")}
exec(HELPER_SOURCE, NAMESPACE)
normalize_result = NAMESPACE["normalize_result"]


class NormalizeResultTests(unittest.TestCase):
    def test_accepts_valid_json_and_exact_quote(self):
        result = normalize_result(
            '{"decision":"approve","reason":"The period is stated.","evidence_quote":"within 30 days"}',
            "Customers may request a refund within 30 days of purchase.",
        )
        self.assertEqual(result["decision"], "approve")
        self.assertEqual(result["evidence_quote"], "within 30 days")

    def test_rejects_quote_not_in_evidence(self):
        result = normalize_result(
            {"decision": "approve", "reason": "Supported.", "evidence_quote": "90 days"},
            "Refunds are available within 30 days.",
        )
        self.assertEqual(result["decision"], "inconclusive")
        self.assertEqual(result["evidence_quote"], "")

    def test_invalid_decision_becomes_inconclusive(self):
        result = normalize_result(
            {"decision": "maybe", "reason": "Unsure.", "evidence_quote": ""},
            "Some evidence.",
        )
        self.assertEqual(result["decision"], "inconclusive")

    def test_non_json_string_becomes_inconclusive(self):
        result = normalize_result("not json", "Some evidence.")
        self.assertEqual(result["decision"], "inconclusive")

    def test_empty_reason_becomes_inconclusive(self):
        result = normalize_result(
            {"decision": "reject", "reason": "  ", "evidence_quote": ""},
            "Some evidence.",
        )
        self.assertEqual(result["decision"], "inconclusive")


if __name__ == "__main__":
    unittest.main()
