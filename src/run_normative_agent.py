"""Utility CLI to run the normative analysis agent against a JSON payload."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from agents.analyse_normative import NormativeAnalysisAgent


def load_payload(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def matches_expected(actual: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    issues: List[str] = []

    if "non_compliance" in expected:
        exp_list = expected.get("non_compliance", [])
        act_list = actual.get("non_compliance", [])
        if len(exp_list) != len(act_list):
            issues.append(
                f"Expected {len(exp_list)} non compliance entries but got {len(act_list)}."
            )
        else:
            for exp_entry in exp_list:
                if not _contains_entry(act_list, exp_entry):
                    issues.append(f"Missing expected non compliance entry: {exp_entry}")

    if "recommendations" in expected:
        exp_reco = expected.get("recommendations", [])
        act_reco = actual.get("recommendations", [])
        for item in exp_reco:
            if item not in act_reco:
                issues.append(f"Missing recommendation: {item}")

    if "data_gaps" in expected:
        exp_gaps = expected.get("data_gaps", [])
        act_gaps = actual.get("quality_checks", {}).get("data_gaps", [])
        for gap in exp_gaps:
            if gap not in act_gaps:
                issues.append(f"Missing data gap note: {gap}")

    return issues


def _contains_entry(entries: List[Dict[str, Any]], expected: Dict[str, Any]) -> bool:
    for entry in entries:
        if all(entry.get(key) == value for key, value in expected.items()):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the normative analysis agent")
    parser.add_argument("payload", type=Path, help="Path to the JSON payload")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print the agent output",
    )
    args = parser.parse_args()

    payload = load_payload(args.payload)
    agent = NormativeAnalysisAgent()
    result = agent.analyse(
        payload.get("intake_payload", {}),
        payload.get("measurements", []),
        payload.get("norm_catalog", []),
    )

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

    expected = payload.get("expected_output")
    if expected is not None:
        issues = matches_expected(result, expected)
        if issues:
            for issue in issues:
                print(f"WARNING: {issue}")
        else:
            print("Expected output matched.")


if __name__ == "__main__":
    main()
