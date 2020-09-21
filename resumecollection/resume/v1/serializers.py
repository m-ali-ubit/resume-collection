from rest_framework import serializers

from resumecollection.resume.models import (
    CandidateProfile,
    Education,
    Experience,
    ContactDetail,
)
from resumecollection.tag_serializer import TagListSerializerField

from django.contrib.auth import get_user_model

User = get_user_model()


class ContactDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetail
        exclude = ("created_at", "last_updated_at")


class EducationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ("created_at", "last_updated_at")


class ExperienceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        exclude = ("created_at", "last_updated_at")


class CandidateProfileSerializer(serializers.ModelSerializer):
    skills = TagListSerializerField(required=False)
    generals = TagListSerializerField(required=False)
    education = EducationModelSerializer(required=False)
    experience = ExperienceModelSerializer(required=False)
    contact_detail = ContactDetailModelSerializer()

    class Meta:
        model = CandidateProfile
        exclude = ("created_at", "last_updated_at")


class CandidateReferenceChainSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SerializerMethodField()

    @staticmethod
    def get_candidate_name(args):
        return f"{args.first_name} {args.last_name}"

    class Meta:
        model = CandidateProfile
        fields = ("id", "candidate_name")
