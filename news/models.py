from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from . utils import sweet_timestamp
import uuid

User = get_user_model()

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    search_params = models.JSONField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if Category.objects.all().count() == 10:
            raise ValidationError("Can't have more than 10 categories")
        super().save(*args, **kwargs)

    @property
    def get_absolute_url(self):
        return reverse('category-articles', args=[str(self.slug)])

    class Meta:
        verbose_name_plural = "Categories"

class Article(models.Model):
    admin = models.ForeignKey(User, related_name="articles", on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    body = RichTextField(config_name="awesome_ckeditor", null=True)
    popular = models.BooleanField(default=False)
    slider = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name="articles", on_delete=models.CASCADE, null=True)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='news/article/images/', null=True)
    video = models.FileField(upload_to='news/article/videos/', null=True, blank=True, storage=VideoMediaCloudinaryStorage)

    timestamp = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(null=True)

    @property
    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.slug)])

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = "/media/pro.png"
        return url

    @property
    def sweet_time_display(self):
        print(self.modified)
        if self.modified:
            return sweet_timestamp(self.modified)
        return sweet_timestamp(self.timestamp)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']    

class ArticleViews(models.Model):
    ip = models.CharField(max_length=250, verbose_name=_("IP Address"))
    article = models.ForeignKey(
        Article, related_name="article_views", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return (
            f"Total views on - {self.article.title} is - {self.article.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Views on Article"
        verbose_name_plural = "Total Article Views"
