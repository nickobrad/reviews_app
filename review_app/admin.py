from django.contrib import admin
from .models import Projects, Profile, Review
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Profile)
admin.site.register(Projects)
admin.site.register(Review)
