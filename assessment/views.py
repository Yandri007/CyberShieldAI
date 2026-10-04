import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from .catalog import AREAS
from .guidance.actions import select_actions
from .guidance.service import generate_guidance
from .rules import AssessmentValidationError, calculate_assessment


@require_GET
@ensure_csrf_cookie
def index(request):
    return render(
        request,
        "assessment/index.html",
        {
            "areas": AREAS,
            "analyze_url": "/api/assessment/analyze/",
        },
    )


@require_POST
def analyze(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "The assessment request was not valid JSON."}, status=400
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "Please send all eight assessment answers."}, status=400
        )

    try:
        result = calculate_assessment(payload.get("answers"))
    except AssessmentValidationError as error:
        response = {"error": str(error)}
        if error.question_id:
            response["question_id"] = error.question_id
        return JsonResponse(response, status=400)

    return JsonResponse(result, json_dumps_params={"ensure_ascii": False})


@require_POST
def guidance(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "The guidance request was not valid JSON."}, status=400
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "Please send all eight assessment answers."}, status=400
        )

    try:
        assessment = calculate_assessment(payload.get("answers"))
    except AssessmentValidationError as error:
        response = {"error": str(error)}
        if error.question_id:
            response["question_id"] = error.question_id
        return JsonResponse(response, status=400)

    selected_actions = select_actions(assessment)
    context = {
        "answers": {area["id"]: area["answer"] for area in assessment["areas"]},
        "assessment": assessment,
        "actions": selected_actions,
    }
    return JsonResponse(generate_guidance(context), json_dumps_params={"ensure_ascii": False})
