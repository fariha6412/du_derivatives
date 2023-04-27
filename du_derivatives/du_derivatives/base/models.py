from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=100, default='')
    profile_picture = models.ImageField(null=True, default='person.png')
    csedu_batch = models.IntegerField(default='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'csedu_batch']

    def __str__(self):
        return self.name


class ProjectType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Create your models here.
class Project(models.Model):
    developer = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    type = models.ForeignKey(ProjectType, on_delete=models.CASCADE, default='')
    date_added = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(auto_now=True)
    github_link = models.CharField(max_length=300, null=True, blank=True)
    demo_link = models.CharField(max_length=300, null=True, blank=True)
    rate = models.IntegerField(default=0)
    about = models.TextField(blank=True, null=True)
    deployed_link = models.CharField(max_length=300)
    logo_img = models.ImageField(null=True, default='noImg.jpeg')
    tags = models.TextField(blank=True, null=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators')

    def __str__(self):
        return self.title


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(unique=True, default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default='')


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default='')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, default='')


class Reply(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    details = models.TextField(default='')


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    star = models.IntegerField(default=0)
