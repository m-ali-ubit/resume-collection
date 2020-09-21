import logging

import django_filters
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from resumecollection.mixins import StandardResultsSetPagination
from resumecollection.resume.models import CandidateProfile
from resumecollection.resume.v1.filters import ProfileFilter, search_filters_list
from resumecollection.resume.v1.serializers import (
    CandidateProfileSerializer,
    CandidateProfileDetailSerializer,
)

logger = logging.getLogger(__name__)


class CandidateProfileView(ModelViewSet):
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filter_class = ProfileFilter
    pagination_class = StandardResultsSetPagination
    search_fields = search_filters_list

    def get_serializer_class(self):
        if self.action == "list":
            return CandidateProfileSerializer
        return CandidateProfileDetailSerializer

    permission_classes = ()
    authentication_classes = ()

    @action(detail=False)
    def get_candidate_chain_references(self, request, **kwargs):
        try:
            candidate_id = kwargs.get("pk")
            if candidate_id:
                candidate_object = get_object_or_404(CandidateProfile, id=candidate_id)
                reference_chain = candidate_object.get_reference_chain()
                reference_chain_serializer = CandidateProfileDetailSerializer(instance=reference_chain, many=True)
                return Response(data=reference_chain_serializer.data, status=status.HTTP_200_OK)
            raise Exception("Candidate id not found")
        except Http404:
            return Response(
                data=f"The candidate with the provided id does not exist.",
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                data=str(err),
                status=status.HTTP_400_BAD_REQUEST,
            )