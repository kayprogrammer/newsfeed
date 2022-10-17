from email.policy import default
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from multiselectfield import MultiSelectField
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField

from . utils import Util
import uuid

ARTICLE_STATUS = (
    ('LATEST', 'LATEST'),
    ('POPULAR', 'POPULAR')
)

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    search_params = models.JSONField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        
class Article(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=200, null=True)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    body = RichTextField(config_name="awesome_ckeditor", null=True)
    status = MultiSelectField(max_length=10, choices=ARTICLE_STATUS, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to='news/article/', null=True)
    video = models.ImageField(upload_to='news/article/', null=True, blank=True)

    timestamp = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

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
    def sweet_ts(self):
        return Util.sweet_timestamp(self.timestamp)

    @property
    def sweet_mod(self):
        return Util.sweet_timestamp(self.modified)

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
