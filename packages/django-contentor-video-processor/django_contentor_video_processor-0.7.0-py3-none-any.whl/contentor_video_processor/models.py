from urllib.parse import urlparse, unquote

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from contentor_video_processor.fields import FormResumableFileField
from contentor_video_processor.functions import process_video
from contentor_video_processor.widgets import ResumableAdminWidget


class AsyncFileField(models.FileField):

    def formfield(self, **kwargs):
        defaults = {"form_class": FormResumableFileField}
        if self.model and self.name:
            defaults["widget"] = ResumableAdminWidget(
                attrs={"model": self.model, "field_name": self.name}
            )
        kwargs.update(defaults)
        return super(AsyncFileField, self).formfield(**kwargs)


class ContentorVideoField(AsyncFileField):
    def __init__(self, *args, allowed_formats=None, max_size_mb=None, resolutions=None, **kwargs):
        self.allowed_formats = allowed_formats or []  # Empty = allow anything
        self.max_size_mb = max_size_mb or 3000  # Default to 3GB
        self.resolutions = resolutions or settings.CONTENTOR_VIDEO_RESOLUTIONS
        super().__init__(*args, **kwargs)

    def clean(self, value, model_instance):
        file = value.file

        # Validate file extension (if specified)
        if self.allowed_formats:
            ext = file.name.split('.')[-1].lower()
            if ext not in self.allowed_formats:
                raise ValidationError(f"Only files with extensions {', '.join(self.allowed_formats)} are allowed.")

        # Validate file size
        if file.size > self.max_size_mb * 1024 * 1024:
            raise ValidationError(f"File size must be smaller than {self.max_size_mb}MB.")

        return super().clean(value, model_instance)


class ContentorVideoModelMixin(models.Model):

    class Meta:
        abstract = True

    def get_video_file_field(self):
        for field in self._meta.fields:
            if isinstance(field, ContentorVideoField):
                return field.name
        return None

    def create_video_processing_objects(self):
        if not self.video:
            return

        video_url = self.video.url

        video_parsed = urlparse(video_url)
        original_path = unquote(video_parsed.path)
        download_url = f"{video_parsed.scheme}://{video_parsed.netloc}{original_path}"

        resolutions = settings.CONTENTOR_VIDEO_RESOLUTIONS

        for resolution in resolutions:
            # If resolution is not 'original', modify the upload URL
            if resolution == "original":
                upload_url = download_url
                resolution = None
            else:
                upload_url = download_url.replace("original", resolution)

            object = VideoProcessingRequest.objects.create(
                video=self,
                download_url=download_url,
                upload_url=upload_url,
                download_provider=settings.CONTENTOR_VIDEO_PROCESSING_DOWNLOAD_PROVIDER,
                upload_provider=settings.CONTENTOR_VIDEO_PROCESSING_UPLOAD_PROVIDER,
                webhook_url="",
                history={},
            )

            if resolution:
                object.resolution = resolution
                object.save(update_fields=["resolution"])

    def save(self, skip_processing=False, *args, **kwargs):
        is_new = self.pk is None
        video_field = self.get_video_file_field()
        file_has_changed = False

        if self.pk and video_field:
            old = self.__class__.objects.get(pk=self.pk)
            file_has_changed = getattr(old, video_field) != getattr(self, video_field)

        if is_new or file_has_changed:
            # Here you can add code to handle the file change
            # For example, trigger transcoding for each resolution
            if not skip_processing:
                self.create_video_processing_objects()
        super().save(*args, **kwargs)

# MetaClass to handle dynamic field creation
class ContentorVideoModelBase(models.base.ModelBase):

    def __new__(mcs, name, bases, attrs):
        # First create the class
        cls = super().__new__(mcs, name, bases, attrs)

        # Only apply to subclasses of ContentorVideoModelMixin, not the mixin itself
        if name == 'ContentorVideoModelMixin':
            return cls

        # Find ContentorVideoField instances in the class
        video_fields = []
        for field_name, field in attrs.items():
            if isinstance(field, ContentorVideoField):
                video_fields.append((field_name, field))

        # Add resolution-specific fields for each video field
        for field_name, field in video_fields:
            for resolution in field.resolutions:
                if resolution == "original":
                    continue

                # Remove 'p' for field name if present (e.g., '720p' -> '720')

                # Add path field
                video_field_name = f"video_{resolution}"
                if not hasattr(cls, video_field_name):
                    video_field = models.FileField(
                        null=True,
                        blank=True,
                        editable=False,
                        upload_to=f"videos/{resolution}",
                        help_text="Yalnızca mov veya mp4 formatında, 3GB'den küçük dosyalar yükleyiniz.",
                    )
                    cls.add_to_class(video_field_name, video_field)

        return cls


class ContentorVideoModel(ContentorVideoModelMixin, models.Model, metaclass=ContentorVideoModelBase):

    class Meta:
        abstract = True


class VideoProcessingRequest(models.Model):
    uuid = models.UUIDField(blank=True, null=True, editable=False)
    video = models.ForeignKey(
        settings.CONTENTOR_VIDEO_MODEL, related_name="processing_jobs", on_delete=models.CASCADE
    )
    output_file_size_mb = models.FloatField(verbose_name="Output File Size (MB)", null=True, blank=True)
    video_duration = models.FloatField(verbose_name="Duration (seconds)", null=True, blank=True)
    metadata = models.JSONField(default=dict)

    RESOLUTION_CHOICES = [
        ("2160p", "2160p (4K)"),
        ("1080p", "1080p (Full HD)"),
        ("720p", "720p (HD)"),
        ("480p", "480p (SD)"),
        ("360p", "360p (Low)"),
    ]
    resolution = models.CharField(
        max_length=5, choices=RESOLUTION_CHOICES, default="1080p"
    )

    download_url = models.URLField(max_length=500, blank=True, null=True)
    upload_url = models.URLField(max_length=500, blank=True, null=True)

    download_provider = models.CharField(max_length=100, blank=True, null=True)
    upload_provider = models.CharField(max_length=100, blank=True, null=True)

    webhook_url = models.URLField(max_length=500, blank=True, null=True)

    history = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=50, default="pending")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = settings.CONTENTOR_PROCESSING_REQUEST_MODEL_VERBOSE_NAME
        verbose_name_plural = settings.CONTENTOR_PROCESSING_REQUEST_MODEL_VERBOSE_NAME_PLURAL

    def __str__(self):
        return f"Processing Job for Video {self.video_id} [{self.id}]"

    def process_video(self):
        self.uuid = process_video(
            download_url=self.download_url,
            upload_url=self.upload_url,
            resolution=self.resolution,
        )
        self.save(update_fields=["uuid"], skip_process=True)  # Only updates the uuid field

    def save(self, skip_process=False, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.uuid and not skip_process:
            self.process_video()