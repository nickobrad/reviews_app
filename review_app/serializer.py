from rest_framework import serializers
from .models import Profile, Projects

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'gender', 'phone_number', 'projects',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'title', 'image', 'description', 'live_link', 'posted_by', 'date_published')

#     design = Rating.objects.filter(project_id=id).values_list('design',flat=True)