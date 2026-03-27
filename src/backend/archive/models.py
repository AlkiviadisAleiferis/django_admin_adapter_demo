from django.conf import settings
from django.db import models

from backend.common.models import DocumentType, TimeStampedModel
from backend.utils.files import get_file_upload_path
from backend.utils.validators import clean_file_field


class File(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, default="")
    file = models.FileField(max_length=255, upload_to=get_file_upload_path)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="uploaded_files",
        on_delete=models.SET_NULL,
    )
    description = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name

    def get_upload_path(self, filename):
        return f"file/none/{filename}"

    def clean(self):
        clean_file_field(self, "file")

    class Meta:
        db_table = "file"


class Image(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, default="")
    img = models.ImageField(max_length=255, upload_to=get_file_upload_path)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="uploaded_images",
        on_delete=models.SET_NULL,
    )
    description = models.TextField(default="", blank=True)

    class Meta:
        db_table = "image"

    def __str__(self):
        return self.name

    def get_upload_path(self, filename):
        return f"image/none/{filename}"

    def clean(self):
        clean_file_field(self, "img")


class Document(TimeStampedModel):
    document_type = models.ForeignKey(
        DocumentType, on_delete=models.CASCADE, related_name="documents"
    )
    identifier = models.CharField(max_length=50)
    issuer = models.CharField(max_length=50, default="", blank=True)
    issued_at = models.DateField(null=True, blank=True)
    expires_at = models.DateField(null=True, blank=True)
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        related_name="uploaded_documents",
        on_delete=models.SET_NULL,
    )

    class Meta:
        db_table = "document"

    def __str__(self):
        return self.identifier


class DocumentFile(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, default="")
    file = models.FileField(max_length=255, upload_to=get_file_upload_path)
    notes = models.TextField(max_length=300, blank=True, default="")

    class Meta:
        db_table = "document_file"
        verbose_name_plural = "Document file"

    def get_upload_path(self, filename):
        return f"document/{self.document.pk}/{filename}"

    def clean(self):
        clean_file_field(self, "file")


class DocumentImage(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, default="")
    img = models.ImageField(max_length=255, upload_to=get_file_upload_path)
    notes = models.TextField(max_length=300, blank=True, default="")

    class Meta:
        db_table = "document_image"
        verbose_name_plural = "Document image"

    def get_upload_path(self, filename):
        return f"document/{self.document.pk}/{filename}"

    def clean(self):
        clean_file_field(self, "img")
