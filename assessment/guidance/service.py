"""Provider-neutral guidance contract, validation, and fallback behavior."""

import os

from django.conf import settings


AI_UNAVAILABLE_NOTICE = (
    "AI guidance is temporarily unavailable, but your security assessment is ready."
)

SUMMARY_COPY = {
    "reassuring": {
        "findings": "These practical next steps follow the findings and priorities from your answers.",
        "preventive": (
            "Your answers did not identify significant gaps. These preventive steps can help "
            "maintain the controls you reported."
        ),
    },
    "direct": {
        "findings": "Start with these actions, selected in the priority order set by your answers.",
        "preventive": "Use these preventive steps to maintain the controls you reported.",
    },
}

EXPLANATION_PREFIX = {
    "confirmed": "Your answer identifies a confirmed gap. ",
    "verification": (
        "Your answer means this control needs checking; it does not confirm that it is missing. "
    ),
    "preventive": "You reported this practice in place. ",
}


def _materialize_actions(actions, styles=None):
    styles = styles or {}
    return [
        {
            "action_id": action["action_id"],
            "kind": action["kind"],
            "kind_label": action["kind_label"],
            "risk_id": action["risk_id"],
            "risk_addressed": action["risk_addressed"],
            "priority": action["priority"],
            "priority_label": action["priority_label"],
            "certainty": action["certainty"],
            "certainty_label": action["certainty_label"],
            "what_to_do": action["what_to_do"],
            "why_it_matters": (
                EXPLANATION_PREFIX[
                    "preventive" if action["certainty"] is None else action["certainty"]
                ]
                + action["why_it_matters"]
                if styles.get(action["action_id"]) == "contextual"
                else action["why_it_matters"]
            ),
            "how_to_start": action["how_to_start"],
        }
        for action in actions
    ]


def _fallback(context):
    assessment = context["assessment"]
    if assessment["findings"]:
        summary = "These practical next steps follow the findings and priorities from your answers."
    else:
        summary = (
            "Your answers did not identify significant gaps. These preventive steps can help "
            "maintain the controls you reported."
        )

    return {
        "mode": "fallback",
        "summary": summary,
        "actions": _materialize_actions(context["actions"]),
        "notice": AI_UNAVAILABLE_NOTICE,
        "can_retry": True,
    }


def _validate_provider_result(result, selected_actions):
    if not isinstance(result, dict) or set(result) != {"summary_style", "actions"}:
        raise ValueError("The guidance response has unexpected fields.")

    summary_style = result["summary_style"]
    returned_actions = result["actions"]
    if summary_style not in SUMMARY_COPY:
        raise ValueError("The guidance response selected an unknown summary style.")
    if not isinstance(returned_actions, list) or len(returned_actions) != len(selected_actions):
        raise ValueError("The guidance response does not match the selected plan.")

    expected_ids = [action["action_id"] for action in selected_actions]
    explanations = {}
    for item in returned_actions:
        if not isinstance(item, dict) or set(item) != {"action_id", "explanation_style"}:
            raise ValueError("A guidance item has unexpected fields.")
        action_id = item["action_id"]
        if action_id not in expected_ids or action_id in explanations:
            raise ValueError("The guidance response changed the selected actions.")
        if item["explanation_style"] not in {"standard", "contextual"}:
            raise ValueError("The guidance response selected an unknown explanation style.")
        explanations[action_id] = item["explanation_style"]

    if set(explanations) != set(expected_ids):
        raise ValueError("The guidance response omitted a selected action.")
    return summary_style, explanations


def _default_adapter():
    if settings.AI_PROVIDER != "openai":
        return None
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None

    # Import the vendor SDK only inside this adapter boundary.
    from .openai_adapter import OpenAIAdapter

    return OpenAIAdapter(api_key=api_key, model=settings.OPENAI_MODEL)


def generate_guidance(context, adapter=None):
    """Personalize only Django-selected actions; use fixed copy on every failure.

    An adapter has one method, ``explain(context)``, and returns only approved
    style identifiers keyed to Django-selected action IDs.
    """
    try:
        provider = adapter if adapter is not None else _default_adapter()
        if provider is None:
            return _fallback(context)

        result = provider.explain(context)
        summary_style, styles = _validate_provider_result(result, context["actions"])
        summary_type = "findings" if context["assessment"]["findings"] else "preventive"
        return {
            "mode": "ai",
            "summary": SUMMARY_COPY[summary_style][summary_type],
            "actions": _materialize_actions(context["actions"], styles),
            "notice": None,
            "can_retry": False,
        }
    except Exception:
        # Provider errors and unusable output must never take down the plan.
        return _fallback(context)
