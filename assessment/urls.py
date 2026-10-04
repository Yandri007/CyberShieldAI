from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="assessment-home"),
    path("api/assessment/analyze/", views.analyze, name="analyze-assessment"),
    path("api/assessment/guidance/", views.guidance, name="assessment-guidance"),
]
