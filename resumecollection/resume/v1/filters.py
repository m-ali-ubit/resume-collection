import django_filters

from taggit.forms import TagField

from resumecollection.resume.models import CandidateProfile


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "in")
        super().__init__(*args, **kwargs)


class ProfileFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id")
    first_name = django_filters.CharFilter("first_name", lookup_expr="icontains")
    last_name = django_filters.CharFilter("last_name", lookup_expr="icontains")
    skills = TagFilter(field_name="skills__name")
    generals = TagFilter(field_name="generals__name")
    email = django_filters.CharFilter("contact_detail__email", lookup_expr="icontains")
    phone_number = django_filters.CharFilter(
        "contact_detail__phone_number", lookup_expr="icontains"
    )
    degree = django_filters.CharFilter("education__degree", lookup_expr="icontains")

    class Meta:
        model = CandidateProfile
        fields = [
            "id",
            "first_name",
            "last_name",
            "skills",
            "generals",
            "email",
            "phone_number",
            "degree",
        ]


search_filters_list = [
    "id",
    "first_name",
    "last_name",
    "contact_detail__email",
    "contact_detail__phone_number",
    "education__degree",
]
