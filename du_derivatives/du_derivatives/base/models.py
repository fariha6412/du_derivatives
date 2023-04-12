from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    email = models.EmailField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100, default='')
    profile_picture = models.ImageField(null=True, default='person.png')
    csedu_batch = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'csedu_batch']


# Create your models here.
class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    date_last_updated = models.DateTimeField(auto_now=True)
    github_link = models.CharField(max_length=300, null=True, blank=True)
    demo_link = models.CharField(max_length=300, null=True, blank=True)
    rate = models.IntegerField(default=0)
    about = models.TextField(blank=True, null=True)
    deployed_link = models.CharField(max_length=300)
    logo_img = models.ImageField(null=True, default='noImg.jpeg')

    def __str__(self):
        return self.title


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProjectTag(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(unique=True, default='')
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(default="")
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    email_address = models.ForeignKey(User, on_delete=models.CASCADE, default='')


class Reply(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    details = models.TextField(default='')


class Rating(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    email_address = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    start = models.IntegerField(default=0)


class Collaborator(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=0)
    email_address = models.ForeignKey(User, on_delete=models.CASCADE, default='')
