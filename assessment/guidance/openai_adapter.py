"""OpenAI Responses API adapter for constrained action-plan explanations."""

import json

from openai import OpenAI


INSTRUCTIONS = """Choose approved wording styles for a small-business cybersecurity action plan.

Use only the supplied categorical answers, canonical assessment results, and Django-selected actions. Django has already determined the score, findings, priorities, order, and action mapping. Do not generate prose, numbers, risk claims, actions, or recommendations. Return only the approved style identifiers and the exact selected action IDs required by the schema.

Choose a summary_style and one explanation_style per selected action. Use contextual only when answer-aware framing would help; Django will supply the approved wording. Repeat every selected action_id exactly once. Do not add or remove actions."""


class OpenAIAdapter:
    """Small provider adapter; core assessment code does not depend on OpenAI."""

    def __init__(self, api_key, model, client=None):
        self.model = model
        self.client = client if client is not None else OpenAI(
            api_key=api_key,
            timeout=20.0,
            max_retries=0,
        )

    @staticmethod
    def _context_payload(context):
        assessment = context["assessment"]
        return {
            "answers": context["answers"],
            "assessment": {
                "score": assessment["score"],
                "status": assessment["status"],
                "findings": [
                    {
                        "risk_id": finding["risk_id"],
                        "area": finding["area"],
                        "priority": finding["priority"],
                        "certainty": finding["certainty"],
                        "reason": finding["reason"],
                    }
                    for finding in assessment["findings"]
                ],
            },
            "selected_actions": [
                {
                    "action_id": action["action_id"],
                    "kind": action["kind"],
                    "risk_id": action["risk_id"],
                    "risk_addressed": action["risk_addressed"],
                    "priority": action["priority"],
                    "certainty": action["certainty"],
                    "what_to_do": action["what_to_do"],
                    "why_it_matters": action["why_it_matters"],
                    "how_to_start": action["how_to_start"],
                }
                for action in context["actions"]
            ],
        }

    @staticmethod
    def _schema(action_ids):
        action_schema = {
            "type": "object",
            "properties": {
                "action_id": {"type": "string", "enum": action_ids},
                "explanation_style": {
                    "type": "string",
                    "enum": ["standard", "contextual"],
                },
            },
            "required": ["action_id", "explanation_style"],
            "additionalProperties": False,
        }
        return {
            "type": "object",
            "properties": {
                "summary_style": {
                    "type": "string",
                    "enum": ["reassuring", "direct"],
                },
                "actions": {"type": "array", "items": action_schema},
            },
            "required": ["summary_style", "actions"],
            "additionalProperties": False,
        }

    def explain(self, context):
        action_ids = [action["action_id"] for action in context["actions"]]
        if not action_ids or len(action_ids) != len(set(action_ids)):
            raise ValueError("The selected action IDs are invalid.")

        response = self.client.responses.create(
            model=self.model,
            instructions=INSTRUCTIONS,
            input=json.dumps(self._context_payload(context), ensure_ascii=False),
            store=False,
            max_output_tokens=300,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "cybershield_guidance",
                    "strict": True,
                    "schema": self._schema(action_ids),
                }
            },
        )
        if getattr(response, "status", None) != "completed":
            raise ValueError("The model did not complete the guidance response.")
        output = getattr(response, "output_text", None)
        if not isinstance(output, str) or not output.strip():
            raise ValueError("The model returned no guidance text.")
        return json.loads(output)
