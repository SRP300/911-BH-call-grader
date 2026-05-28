from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class DimensionRubric:
    name: str
    weight_percent: float


DIMENSIONS: List[DimensionRubric] = [
    # Dimensions aligned to the example grading PDF table.
    DimensionRubric(name="Address & Location", weight_percent=10.0),
    DimensionRubric(name="Medical Assessment", weight_percent=15.0),
    DimensionRubric(name="Naloxone Inquiry", weight_percent=15.0),
    DimensionRubric(name="Pre-Arrival Instructions", weight_percent=15.0),
    DimensionRubric(name="Good Samaritan Disclosure", weight_percent=10.0),
    DimensionRubric(name="Dispatch Accuracy", weight_percent=10.0),
    DimensionRubric(name="Behavioral Health Diversion", weight_percent=10.0),
    DimensionRubric(name="Caller Management", weight_percent=10.0),
    DimensionRubric(name="Information Completeness", weight_percent=5.0),
]


@dataclass(frozen=True)
class EvidenceAndNotes:
    evidence: str
    notes: str


@dataclass(frozen=True)
class DimensionScore:
    name: str
    weight_percent: float
    score_out_of_5: float
    evidence_and_notes: EvidenceAndNotes


@dataclass(frozen=True)
class CallMetadata:
    call_id: str
    date: str
    operator: str
    duration: str
    call_type: str
    assessed_by: str = "AI Quality Assurance"
    system_label: str = "System"


@dataclass(frozen=True)
class CallGradingReport:
    title: str
    subtitle: str
    metadata: CallMetadata
    overall_score_out_of_5: float
    rating_label: str
    dimension_scores: List[DimensionScore]
    strengths: List[str]
    areas_for_improvement: List[str]
    critical_flags: List[str]
    coaching_recommendation: str
    footer_disclaimer: str


def rating_from_score(overall_score_out_of_5: float) -> str:
    # Matches the example PDF style (Excellent vs Needs Improvement).
    if overall_score_out_of_5 >= 4.0:
        return "Excellent"
    if overall_score_out_of_5 >= 2.5:
        return "Satisfactory"
    return "Needs Improvement"


def _require(obj: Dict[str, Any], key: str) -> Any:
    if key not in obj:
        raise ValueError(f"Missing required key: {key}")
    return obj[key]


def compute_weighted_overall_score(dimension_scores: List[DimensionScore]) -> float:
    """
    Deterministic overall score: weighted average of per-dimension scores.
    Weights are the rubric weights (sum to 100).
    """
    if not dimension_scores:
        raise ValueError("dimension_scores is empty")
    total_weight = sum(ds.weight_percent for ds in dimension_scores)
    if total_weight <= 0:
        raise ValueError("total_weight must be positive")
    weighted = sum(ds.score_out_of_5 * ds.weight_percent for ds in dimension_scores) / total_weight
    # Clamp to [0, 5] and round to 1 decimal to match the template style.
    weighted = max(0.0, min(5.0, weighted))
    return round(weighted, 1)


def parse_scorecard(scorecard_json: Dict[str, Any], *, metadata: CallMetadata) -> CallGradingReport:
    # We compute overall deterministically from dimension scores to standardize grading.
    # Keep reading the model-provided overall if present, but ignore it for final output.
    _ = scorecard_json.get("overall_score_out_of_5", None)
    dimension_scores_raw = _require(scorecard_json, "dimension_scores")
    if not isinstance(dimension_scores_raw, list):
        raise ValueError("dimension_scores must be a list")

    dim_by_name = {d.name: d for d in DIMENSIONS}
    dimension_scores: List[DimensionScore] = []

    for row in dimension_scores_raw:
        if not isinstance(row, dict):
            raise ValueError("Each dimension score row must be an object")
        name = str(_require(row, "name"))
        rubric = dim_by_name.get(name)
        if not rubric:
            raise ValueError(f"Unknown dimension name: {name}")

        score_out_of_5 = float(_require(row, "score_out_of_5"))
        ev = _require(row, "evidence_and_notes")
        if not isinstance(ev, dict):
            raise ValueError(f"evidence_and_notes for {name} must be an object")
        evidence = str(_require(ev, "evidence"))
        notes = str(_require(ev, "notes"))

        dimension_scores.append(
            DimensionScore(
                name=name,
                weight_percent=rubric.weight_percent,
                score_out_of_5=score_out_of_5,
                evidence_and_notes=EvidenceAndNotes(evidence=evidence, notes=notes),
            )
        )

    # Basic presence checks. Prototype scoring should cover all dimensions.
    found_names = {ds.name for ds in dimension_scores}
    missing = [d.name for d in DIMENSIONS if d.name not in found_names]
    if missing:
        raise ValueError(f"Missing dimension scores: {missing}")

    strengths = _require(scorecard_json, "strengths")
    if not isinstance(strengths, list):
        raise ValueError("strengths must be a list")

    areas = _require(scorecard_json, "areas_for_improvement")
    if not isinstance(areas, list):
        raise ValueError("areas_for_improvement must be a list")

    critical = _require(scorecard_json, "critical_flags")
    if not isinstance(critical, list):
        raise ValueError("critical_flags must be a list")

    coaching = _require(scorecard_json, "coaching_recommendation")
    if not isinstance(coaching, str):
        raise ValueError("coaching_recommendation must be a string")

    footer = _require(
        scorecard_json,
        "footer_disclaimer",
    )
    if not isinstance(footer, str):
        raise ValueError("footer_disclaimer must be a string")

    overall_score = compute_weighted_overall_score(dimension_scores)
    rating_label = rating_from_score(overall_score)

    rubric_index = {d.name: i for i, d in enumerate(DIMENSIONS)}

    return CallGradingReport(
        title="911 CALL QUALITY ASSESSMENT",
        subtitle="Behavioral Health Call Quality Assessment Report",
        metadata=metadata,
        overall_score_out_of_5=overall_score,
        rating_label=rating_label,
        dimension_scores=sorted(dimension_scores, key=lambda x: rubric_index[x.name]),
        strengths=[str(x) for x in strengths],
        areas_for_improvement=[str(x) for x in areas],
        critical_flags=[str(x) for x in critical],
        coaching_recommendation=str(coaching),
        footer_disclaimer=str(footer),
    )

