from rest_framework import serializers

from resumecollection.resume.models import (
    CandidateProfile,
    Education,
    Experience,
    ContactDetail,
)
from resumecollection.tag_serializer import TagListSerializerField


class ContactDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        fields = "__all__"


class EducationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class ExperienceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"


class CandidateProfileSerializer(serializers.ModelSerializer):
    skills = TagListSerializerField(required=False)
    generals = TagListSerializerField(required=False)
    education = EducationModelSerializer(required=False)
    experience = ExperienceModelSerializer(required=False)
    contact_detail = ContactDetailModelSerializer()

    class Meta:
        model = CandidateProfile
        fields = "__all__"
