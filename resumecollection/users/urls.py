from django.urls import path, include

app_name = "users"
urlpatterns = [
    path("", include("resumecollection.users.v1.urls"))
]
