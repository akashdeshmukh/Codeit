from django.db import models
from django.utils import timezone
import datetime


class Post(models.Model):
    """
    Model represents each post individually for blog
    @post_name => post NAME
    @post_text => post text
    @pub_date  => date on which post is published
    """
    post_name = models.CharField(max_length=200)
    post_text = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.post_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
