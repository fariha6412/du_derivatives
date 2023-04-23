from django.contrib import admin
from .models import Project, Photo, User, Reply, Review, Rating, ProjectType

# Register your models here.
admin.site.register(Project)
admin.site.register(Photo)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(User)
admin.site.register(ProjectType)