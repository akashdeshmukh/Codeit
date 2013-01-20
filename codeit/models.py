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
    pub_date = models.DateTimeField("date published")

    def __unicode__(self):
        return self.post_name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"


class User(models.Model):
    """
    """
    receipt_no = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    total_points = models.IntegerField()
    year = models.CharField(max_length=5)
    isactive = models.BooleanField(default=False)

    def user_active(self):
        return self.isactive
    user_active.admin_order_field = "isactive"
    user_active.boolean = True
    user_active.short_description = "Active now ?"

    def fullname(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __unicode__(self):
        return str(self.first_name) + " " + str(self.last_name)


def problem_function(instance, filename):
    return "/".join(["problem", filename])


class Problem(models.Model):
    """
    """
    name = models.CharField(max_length=150)
    statement = models.TextField()
    year = models.IntegerField()
    points = models.IntegerField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    standard_input = models.FileField(upload_to=problem_function)
    standard_output = models.FileField(upload_to=problem_function)

    def __unicode__(self):
        return self.name


def my_function(instance, filename):
    filename = filename.split(".")
    path = "/".join(["documents", str(instance.user.receipt_no), instance.problem.name + "-"
        + str(filename[0]) + "." + instance.language.lower()])
    path = path.replace(" ", "")
    return path


class Solution(models.Model):
    """
    """
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User)
    text = models.FileField(upload_to=my_function)
    language = models.CharField(max_length=20)
    points_obtained = models.IntegerField()

    def __unicode__(self):
        return str(self.problem) + " " + str(self.user)


