"""Synthetic teaching example for Research Note 001. Python 3.10+; stdlib only.

Run: python binding_example.py
No private data, network, file writes, authority or admission actions.
The local recorder and this process are trusted. Receipts are in memory only.
"""
import hashlib
import json
from dataclasses import dataclass, replace


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def evaluate(blob: bytes) -> str:
    # The test has deliberately limited coverage; it does not identify a version.
    obj = json.loads(blob)
    return "TEST_PASS" if type(obj.get("value")) is int else "TEST_FAIL"


def unbound_run(run_id: str, blob: bytes) -> dict:
    return {"run_id": run_id, "result": evaluate(blob)}


@dataclass(frozen=True)
class Start:
    run_id: str
    input_sha256: str


@dataclass(frozen=True)
class End:
    run_id: str
    input_sha256: str
    result: str


def captured_run(run_id: str, blob: bytes) -> tuple[Start, End]:
    # Hash and evaluate the SAME immutable bytes. No second path lookup.
    start = Start(run_id, digest(blob))
    result = evaluate(blob)
    return start, End(run_id, start.input_sha256, result)


def binding_check(expected_run: str, proposed: bytes,
                  start: Start | None, end: End | None) -> str:
    if start is None or end is None:
        return "UNKNOWN"
    if start.run_id != expected_run or end.run_id != expected_run:
        return "REJECTED"
    if start.input_sha256 != digest(proposed):
        return "REJECTED"
    if end.input_sha256 != start.input_sha256:
        return "REJECTED"
    # This checks identity consistency, not test success or permission to promote.
    return "BINDING_CHECK_PASS_ONLY"


def main() -> None:
    a = b'{"revision":"A","value":1}'
    b = b'{"revision":"B","value":2}'
    if a == b or digest(a) == digest(b):
        raise AssertionError("Distinct example inputs required")
    world_a = unbound_run("run-7", a)
    world_b = unbound_run("run-7", b)
    if world_a != world_b or world_a["result"] != "TEST_PASS":
        raise AssertionError("Counterexample did not reproduce")
    start, end = captured_run("run-8", a)
    cases = [
        ("missing_input_binding", None, None, a, "UNKNOWN"),
        ("missing_terminal", start, None, a, "UNKNOWN"),
        ("different_candidate", start, end, b, "REJECTED"),
        ("wrong_run", start, replace(end, run_id="run-9"), a, "REJECTED"),
        ("contradictory_terminal", start,
         replace(end, input_sha256=digest(b)), a, "REJECTED"),
        ("matching_binding", start, end, a, "BINDING_CHECK_PASS_ONLY"),
    ]
    results = {}
    for label, pre, terminal, proposed, expected in cases:
        observed = binding_check("run-8", proposed, pre, terminal)
        if observed != expected:
            raise AssertionError((label, observed, expected))
        results[label] = observed
    print(json.dumps({
        "classification": "SYNTHETIC_TEACHING_EXAMPLE",
        "same_unbound_receipt_for_distinct_inputs": world_a == world_b,
        "unbound_receipt": world_a,
        "cases": results,
        "promotion": "NOT_EVALUATED",
        "canonical_transition": "NOT_ATTEMPTED",
        "limitations": "Honest local recorder; no durability or attestation proof"
    }, indent=2))


if __name__ == "__main__":
    main()
