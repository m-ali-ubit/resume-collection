from rest_framework import serializers

from resumecollection.resume.models import CandidateProfile, Education, Experience
from resumecollection.tag_serializer import TagListSerializerField


class CandidateProfileDetailSerializer(serializers.ModelSerializer):
    skills = TagListSerializerField(required=False)
    generals = TagListSerializerField(required=False)
    education = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Education.objects.all()
    )
    experience = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Experience.objects.all()
    )

    class Meta:
        model = CandidateProfile
        fields = "__all__"


class CandidateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProfile
        fields = (
            "id",
            "first_name",
            "last_name",
            "contact_detail",
            "added_by",
        )
