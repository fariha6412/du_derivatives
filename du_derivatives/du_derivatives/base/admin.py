from django.contrib import admin
from .models import Project, Tag, ProjectTag, Photo, User, Collaborator, Reply, Review, Rating
# Register your models here.
admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(ProjectTag)
admin.site.register(Photo)
admin.site.register(Collaborator)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Reply)
admin.site.register(User)