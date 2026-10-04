"""Pure, deterministic scoring and risk-ranking rules."""

from .catalog import (
    ANSWER_LABELS,
    ANSWER_POINTS_QUARTERS,
    AREAS,
    PRIORITY_RANK,
)


class AssessmentValidationError(ValueError):
    def __init__(self, message, question_id=None):
        super().__init__(message)
        self.question_id = question_id


def validate_answers(answers):
    if not isinstance(answers, dict):
        raise AssessmentValidationError("Please provide all eight assessment answers.")

    expected_ids = [area["id"] for area in AREAS]
    for area_id in expected_ids:
        if area_id not in answers or answers[area_id] is None or answers[area_id] == "":
            raise AssessmentValidationError(
                "Please answer this question to continue.", question_id=area_id
            )

    extra_ids = set(answers) - set(expected_ids)
    if extra_ids:
        raise AssessmentValidationError("The assessment contains an unknown question.")

    for area in AREAS:
        answer = answers[area["id"]]
        if not isinstance(answer, str) or answer not in ANSWER_POINTS_QUARTERS:
            raise AssessmentValidationError(
                "Choose Yes, No, or Not sure to continue.", question_id=area["id"]
            )

    return {area_id: answers[area_id] for area_id in expected_ids}


def _status_for_score(score):
    if score >= 80:
        return (
            "strong",
            "Strong",
            "Most important controls appear to be in place, based on your answers.",
        )
    if score >= 50:
        return (
            "needs_attention",
            "Needs Attention",
            "Your answers show meaningful gaps or areas that need verification.",
        )
    return (
        "high_risk",
        "High Risk",
        "Your answers show several important controls that need urgent attention.",
    )


def _finding_for(area, answer):
    if answer == "yes":
        return None

    confirmed = answer == "no"
    priority = "high" if area["impact"] == "high" else "medium"
    certainty = "confirmed" if confirmed else "verification"
    if confirmed:
        reason = area["risk_reason"]
        certainty_label = "Confirmed gap"
    else:
        reason = f"This area needs verification. {area['risk_reason']}"
        certainty_label = "Needs verification"

    return {
        "risk_id": area["id"],
        "area": area["name"],
        "answer": answer,
        "priority": priority,
        "priority_label": "High" if priority == "high" else "Medium",
        "certainty": certainty,
        "certainty_label": certainty_label,
        "reason": reason,
        "action_id": area["action_id"] if confirmed else area["verification_action_id"],
        "area_order": next(
            index for index, candidate in enumerate(AREAS) if candidate["id"] == area["id"]
        ),
    }


def calculate_assessment(answers):
    """Validate answers and return the exact score plus ordered findings.

    Scores are accumulated as quarter-points: Yes=50, Not sure=25, No=0.
    Dividing the integer total by four yields the PRD's exact point values.
    Findings sort by priority, confirmed No before Not sure, then fixed area order.
    """
    canonical_answers = validate_answers(answers)
    score_quarters = 0
    area_results = []
    findings = []

    for area in AREAS:
        answer = canonical_answers[area["id"]]
        points = ANSWER_POINTS_QUARTERS[answer] / 4
        score_quarters += ANSWER_POINTS_QUARTERS[answer]

        if answer == "yes":
            signal = "in_place"
            signal_label = "Reported in place"
        elif answer == "not_sure":
            signal = "needs_verification"
            signal_label = "Needs verification"
        else:
            signal = "confirmed_gap"
            signal_label = "Confirmed gap"

        area_results.append(
            {
                "id": area["id"],
                "name": area["name"],
                "answer": answer,
                "answer_label": ANSWER_LABELS[answer],
                "points": points,
                "signal": signal,
                "signal_label": signal_label,
                "impact": area["impact"],
            }
        )

        finding = _finding_for(area, answer)
        if finding is not None:
            findings.append(finding)

    findings.sort(
        key=lambda finding: (
            PRIORITY_RANK[finding["priority"]],
            0 if finding["certainty"] == "confirmed" else 1,
            finding["area_order"],
        )
    )
    for finding in findings:
        finding.pop("area_order")

    score = score_quarters / 4
    status_id, status, status_description = _status_for_score(score)

    return {
        "score": score,
        "score_label": "Self-reported security-controls score",
        "status_id": status_id,
        "status": status,
        "status_description": status_description,
        "disclaimer": "Based on your answers—not a technical measurement or verification of your security.",
        "areas": area_results,
        "findings": findings,
    }
