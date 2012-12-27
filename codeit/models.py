from django.db import models


class User(models.Model):
    """
    """
    receipt_no = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    total_points = models.IntegerField()
    year = models.CharField(max_length=5)

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

    def __unicode__(self):
        return self.name


class Solution(models.Model):
    """
    """
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User)
    text = models.FileField(upload_to='documents/%Y/%m/%d')
    language = models.CharField(max_length=20)
    points_obtained = models.IntegerField()

    def __unicode__(self):
        return str(self.problem) + " " + str(self.user)
