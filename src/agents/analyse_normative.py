"""Normative analysis agent skeleton for sidewalk accessibility."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class NormativeAgentConfig:
    width_medium_ratio: float = 0.05
    width_high_ratio: float = 0.10
    slope_medium_ratio: float = 0.05
    slope_high_ratio: float = 0.10
    length_tolerance_m: float = 5.0


class NormativeAnalysisAgent:
    """Performs basic checks against PMR accessibility thresholds."""

    def __init__(self, config: Optional[NormativeAgentConfig] = None) -> None:
        self.config = config or NormativeAgentConfig()

    def analyse(
        self,
        intake_payload: Dict[str, Any],
        measurements: List[Dict[str, Any]],
        norm_catalog: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        required_min_width = intake_payload.get("required_min_width_m")
        required_max_slope = intake_payload.get("required_max_slope_percent")
        norm_catalog = norm_catalog or []

        non_compliance: List[Dict[str, Any]] = []
        recommendations: List[str] = []
        data_gaps: List[str] = []

        total_length = 0.0
        for section in measurements:
            chainage = float(section.get("chainage_m", 0.0))
            length = float(section.get("segment_length_m", 0.0))
            end_chainage = chainage + length
            total_length += length

            width = section.get("width_m")
            if width is None:
                data_gaps.append(
                    f"Segment {chainage:.0f}-{end_chainage:.0f} m: width missing"
                )
            elif required_min_width is not None and width < required_min_width:
                severity = self._severity_width(width, required_min_width)
                reference = self._find_norm_reference(norm_catalog, "Largeur")
                non_compliance.append(
                    {
                        "type": "width",
                        "chainage_start_m": chainage,
                        "chainage_end_m": end_chainage,
                        "measured_value": width,
                        "required_min": required_min_width,
                        "severity": severity,
                        "norm_reference": reference,
                    }
                )
                recommendations.append(
                    self._width_recommendation(chainage, end_chainage, required_min_width)
                )

            slope = section.get("longitudinal_slope_percent")
            if slope is None:
                data_gaps.append(
                    f"Segment {chainage:.0f}-{end_chainage:.0f} m: longitudinal slope missing"
                )
            elif required_max_slope is not None and slope > required_max_slope:
                severity = self._severity_slope(slope, required_max_slope)
                reference = self._find_norm_reference(norm_catalog, "Pente")
                non_compliance.append(
                    {
                        "type": "longitudinal_slope",
                        "chainage_start_m": chainage,
                        "chainage_end_m": end_chainage,
                        "measured_value": slope,
                        "required_max": required_max_slope,
                        "severity": severity,
                        "norm_reference": reference,
                    }
                )
                recommendations.append(
                    self._slope_recommendation(chainage, end_chainage, required_max_slope)
                )

        summary = self._build_summary(non_compliance)
        intake_crosscheck = self._check_length(total_length, intake_payload.get("project_length_m"))

        return {
            "summary": summary,
            "non_compliance": non_compliance,
            "recommendations": recommendations,
            "quality_checks": {
                "intake_crosscheck": intake_crosscheck,
                "data_gaps": data_gaps,
            },
            "metrics": {
                "segments_analyzed": len(measurements),
                "non_compliance_count": len(non_compliance),
            },
        }

    def _severity_width(self, measured: float, required: float) -> str:
        ratio = (required - measured) / required
        if ratio >= self.config.width_high_ratio:
            return "high"
        if ratio >= self.config.width_medium_ratio:
            return "medium"
        return "low"

    def _severity_slope(self, measured: float, required: float) -> str:
        ratio = (measured - required) / required if required else 0.0
        if ratio >= self.config.slope_high_ratio:
            return "high"
        if ratio >= self.config.slope_medium_ratio:
            return "medium"
        return "low"

    def _find_norm_reference(self, catalog: List[Dict[str, Any]], keyword: str) -> Optional[str]:
        for item in catalog:
            if keyword.lower() in item.get("requirement", "").lower():
                return item.get("reference")
        return None

    def _width_recommendation(self, start: float, end: float, required: float) -> str:
        return (
            f"Increase sidewalk width between {start:.0f}-{end:.0f} m to at least {required:.2f} m."
        )

    def _slope_recommendation(self, start: float, end: float, required: float) -> str:
        return (
            f"Regrade longitudinal slope between {start:.0f}-{end:.0f} m to maximum {required:.2f} %."
        )

    def _build_summary(self, non_compliance: List[Dict[str, Any]]) -> str:
        if not non_compliance:
            return "No non compliance detected."
        counts: Dict[str, int] = {}
        for item in non_compliance:
            counts[item["type"]] = counts.get(item["type"], 0) + 1
        parts = [f"{count} {item}" for item, count in counts.items()]
        return f"Non compliance detected: {', '.join(parts)}."

    def _check_length(self, total: float, expected: Optional[float]) -> bool:
        if expected is None:
            return False
        return abs(total - float(expected)) <= self.config.length_tolerance_m
