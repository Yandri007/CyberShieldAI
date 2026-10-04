from django.urls import include, path


urlpatterns = [path("", include("assessment.urls"))]
