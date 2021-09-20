from django.db import models
from cloudinary.uploader import upload
from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Projects(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image', blank= True)
    description = HTMLField(blank= True)
    live_link = models.URLField(max_length= 400, blank=True, null= True)
    posted_by = models.ForeignKey(User, related_name='myprojects', on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True) 

    def get_absolute_url(self):
        return reverse('profile')
 
    def __str__(self) -> str:
        return self.title 
 
    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()

    @classmethod
    def update_project_title(cls, project_id, new_title):
        project = cls.objects.filter(id = project_id).update(title = new_title)
        return project

    @classmethod
    def search_by_title(cls,search_term):
        project = cls.objects.filter(title__icontains = search_term)
        return project

class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='myprofile')
    profile_photo = CloudinaryField('image', blank= True)
    projects = models.ForeignKey(Projects, related_name='myprojects', on_delete=models.DO_NOTHING, null=True, blank=True)
    bio = models.TextField(blank=True) 
    gender = models.CharField(max_length=50, null = True)
    phone_number = models.CharField(max_length=100, null = True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True) 

    def get_absolute_url(self):
        return reverse('profile')

    def __str__(self) -> str:
        return self.user.username 

    def save_profile(self):
        return self.save()

    def delete_profile(self):
        return self.delete()

    @classmethod
    def update_profile(cls, profile_id, new_bio):
        profile = cls.objects.filter(id = profile_id).update(bio = new_bio)
        return profile

    @classmethod
    def search_by_username(cls,search_term):
        users = cls.objects.filter(user__username__icontains = search_term)
        return users

REVIEW_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
]

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='reviews')
    design = models.PositiveSmallIntegerField(choices = REVIEW_CHOICES, blank = True, default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    usability = models.PositiveSmallIntegerField(choices = REVIEW_CHOICES, blank = True, default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])
    content = models.PositiveSmallIntegerField(choices = REVIEW_CHOICES, blank = True, default=1, validators=[MinValueValidator(1), MaxValueValidator(10)])

    def save_review(self):
        self.save()

    def delete_review(self):
        self.delete()

    @classmethod
    def update_review_design(cls, review_id, new_review):
        review = cls.objects.filter(id = review_id).update(design = new_review)
        return review

    @classmethod
    def update_review_usability(cls, review_id, new_review):
        review = cls.objects.filter(id = review_id).update(usability = new_review)
        return review

    @classmethod
    def update_review_content(cls, review_id, new_review):
        review = cls.objects.filter(id = review_id).update(content = new_review)
        return review