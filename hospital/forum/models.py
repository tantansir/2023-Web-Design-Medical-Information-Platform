from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    telephone = models.CharField(max_length=500)
    email = models.EmailField()
    district = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    info = models.CharField(max_length=1000)

    def __str__(self):
        return self.user.username


class Hospital(models.Model):
    name = models.CharField(max_length=500)
    telephone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    info = models.TextField()
    advantage_1 = models.CharField(max_length=500, blank=True, null=True, )
    advantage_2 = models.CharField(max_length=500, blank=True, null=True, )
    advantage_3 = models.CharField(max_length=500, blank=True, null=True, )
    district = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=500)
    illness = models.TextField()

    def __str__(self):
        return self.name


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    content = models.TextField()
    pageview = models.IntegerField(default=0)
    collect_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.content


class Collection_Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "blog")


class Collection_Hospital(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "hospital")


class Illness(models.Model):
    alphabet = models.CharField(max_length=10)
    name = models.CharField(max_length=500)
    department = models.CharField(max_length=500)

    def __str__(self):
        return self.name
