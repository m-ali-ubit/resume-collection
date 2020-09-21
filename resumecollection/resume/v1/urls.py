from django.urls import path, include
from rest_framework.routers import DefaultRouter

from resumecollection.resume.v1.views import CandidateProfileView

app_name = "resume"

router = DefaultRouter()

router.register(r"", CandidateProfileView, basename="v1-resume")

urlpatterns = [
    path(
        "<int:pk>/get_candidate_chain_references/",
        CandidateProfileView.as_view({"get": "get_candidate_chain_references"}),
    ),
    path("", include(router.urls)),
]
