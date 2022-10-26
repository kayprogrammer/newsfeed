from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Message(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    body = models.TextField(null=True)
    addressed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class About(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(default="newsfeed@email.com", null=True)
    phone = models.CharField(default="(234) 901 234 5678", max_length=200)
    address = models.TextField(default="NewsFeed, 1238 S . 123 St.Suite 25 Lagos, Nigeria", null=True)
    facebook = models.CharField(default="https://facebook.com", max_length=10000, null=True)
    twitter = models.CharField(default="https://twitter.com", max_length=10000, null=True)
    pinterest = models.CharField(default="https://pinterest.com", max_length=10000, null=True)
    googleplus = models.CharField(default="https://accounts.google.com", max_length=10000, null=True)
    vimeo = models.CharField(default="https://vimeo.com", max_length=10000, null=True)
    youtube = models.CharField(default="https://youtube.com", max_length=10000, null=True)
    flickr = models.CharField(default="https://flickr.com", max_length=10000, null=True)
    mail = models.CharField(default="https://mail.google.com", max_length=10000, null=True)
    
    desc = models.TextField(default="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
        null=True
    )

    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and About.objects.exists():
            raise ValidationError('There can be only one Site detail instance')

        return super(About, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Site Details"
        verbose_name_plural = "Site Details"
