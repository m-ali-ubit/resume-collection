from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from resumecollection.mixins import CreateUpdateMixin

User = get_user_model()


class ContactDetail(CreateUpdateMixin):
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=200, null=True, blank=True)
    linked_in = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.email


class Education(CreateUpdateMixin):
    degree = models.CharField(max_length=100)
    institute = models.CharField(max_length=100)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100)


class Experience(CreateUpdateMixin):
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100)


class TaggedSkills(TaggedItemBase):
    content_object = models.ForeignKey("CandidateProfile", on_delete=models.CASCADE)


class TaggedGenerals(TaggedItemBase):
    content_object = models.ForeignKey("CandidateProfile", on_delete=models.CASCADE)


class CandidateProfile(CreateUpdateMixin):
    first_name = models.CharField(max_length=25)
    middle_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25)
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    contact_detail = models.ForeignKey(ContactDetail, on_delete=models.CASCADE)
    resume = models.FileField(
        upload_to="resume/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "docx"])],
    )
    skills = TaggableManager(
        blank=True, related_name="skills", through=TaggedSkills, verbose_name="Skills"
    )
    generals = TaggableManager(
        blank=True,
        related_name="generals",
        through=TaggedGenerals,
        verbose_name="Generals",
    )
    education = models.ForeignKey(Education, on_delete=models.CASCADE, null=True, blank=True)
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, null=True, blank=True)
    reference = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    def get_reference_chain(self, with_self=True):
        references = []
        if with_self:
            references.append(self)
        for candidate in CandidateProfile.objects.filter(reference=self):
            _references = candidate.get_reference_chain(with_self=True)
            if len(_references):
                references.extend(_references)
        return references

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_at"]
