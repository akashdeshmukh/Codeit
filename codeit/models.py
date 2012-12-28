from django.db import models


class User(models.Model):
    """
    """
    receipt_no = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    total_points = models.IntegerField()
    year = models.CharField(max_length=5)
    isactive = models.BooleanField(default=False)

    def fullname(self):
        return str(self.first_name) + " " + str(self.last_name)

    def __unicode__(self):
        return str(self.first_name) + " " + str(self.last_name)


class Problem(models.Model):
    """
    """
    name = models.CharField(max_length=150)
    statement = models.TextField()
    year = models.IntegerField()
    points = models.IntegerField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    standard_input = models.FileField(upload_to="problem/")
    standard_output = models.FileField(upload_to="problem/")

    def __unicode__(self):
        return self.name


def my_function(instance, filename):
    filename = filename.split(".")
    print instance.user.receipt_no
    return "/".join(["documents", str(instance.user.receipt_no), instance.problem.name + "." + filename[-1]])


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
