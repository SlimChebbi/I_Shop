from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.utils.html import escape


class Feed(models.Model):
    user = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    post = models.TextField(max_length=255)

    class Meta:
        verbose_name = _('Feed')
        verbose_name_plural = _('Feeds')
        ordering = ('-date',)

    def __unicode__(self):
        return self.post

    @staticmethod
    def get_feeds(from_feed=None):
        if from_feed is not None:
            feeds = Feed.objects.filter(id__lte=from_feed)
        else:
            feeds = Feed.objects.filter()
        return feeds

    @staticmethod
    def get_feeds_after(feed):
        feeds = Feed.objects.filter( id__gt=feed)
        return feeds
