from django.contrib import admin

from resumecollection.mixins import ReadOnlyDateMixin
from resumecollection.resume.models import (
    CandidateProfile,
    Education,
    Experience,
    ContactDetail,
)


class CandidateProfileAdmin(ReadOnlyDateMixin):
    model = CandidateProfile
    list_display = ["id", "first_name", "last_name", "added_by"]


class EducationAdmin(ReadOnlyDateMixin):
    list_display = ["id", "degree", "institute"]


class ExperienceAdmin(ReadOnlyDateMixin):
    list_display = ["id", "position", "company"]


class ContactDetailAdmin(ReadOnlyDateMixin):
    list_display = ["id", "phone_number", "email"]


admin.site.register(CandidateProfile, CandidateProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(ContactDetail, ContactDetailAdmin)
