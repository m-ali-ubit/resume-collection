from django.urls import path, include

app_name = "resume"
urlpatterns = [
    path("", include("resumecollection.resume.v1.urls"))
]
