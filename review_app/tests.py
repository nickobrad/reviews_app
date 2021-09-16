from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Projects, Review

# Create your tests here.
class ReviewAppTestClass(TestCase):

    def setUp(self):
        self.new_user = User(id = 1, first_name = 'James', last_name = 'Bond', username = 'jamie', email = 'jamesbond@gmail.com')
        # self.new_user.save()

        self.new_project = Projects(id = 1, title = 'Test', image = 'photo.jpg', description = 'Test project', live_link = 'https://moringaschool.com/', posted_by = self.new_user)
        # self.new_project.save()

        self.new_profile = Profile(id =1, user = self.new_user, profile_photo = 'save.jpg', projects = self.new_project, bio = 'Hi, I am new', gender = 'male', phone_number = '071111111')
        # self.new_profile.save()

        self.new_review = Review(id = 1, reviewer = self.new_user, reviewed_project = self.new_project, design = 1, usability = 1, content = 1)
        # self.new_review.save()

    def tearDown(self):
        User.objects.all().delete()
        Profile.objects.all().delete()
        Projects.objects.all().delete()
        Review.objects.all().delete()

    def test_instance_user(self):
        self.assertTrue(isinstance(self.new_user, User))

    def test_instance_project(self):
        self.assertTrue(isinstance(self.new_project, Projects))

    def test_instance_review(self):
        self.assertTrue(isinstance(self.new_review, Review))

    def test_instance_profile(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_profile(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile) > 0)
    
    def test_save_project(self):
        self.new_project.save_project()
        projects = Projects.objects.all()
        self.assertTrue(len(projects) > 0)

    def test_save_review(self):
        self.new_review.save_review()
        review = Review.objects.all()
        self.assertTrue(len(review) > 0)

    def test_delete_profile(self):
        profile = self.new_profile
        profile.save_profile()
        profile.delete_profile()        
        self.assertTrue(len(Profile.objects.all()) == 0)

    def test_delete_project(self):
        project = self.new_project
        project.save()
        project.delete_project()
        self.assertTrue(len(Projects.objects.all()) == 0)

    def test_delete_review(self):
        review = self.new_review
        review.save_review()
        review.delete_review()        
        self.assertTrue(len(Review.objects.all()) == 0)

    def test_update_profile(self):
        self.new_profile.save()
        profile_id = Profile.objects.last().id
        Profile.update_profile(profile_id, 'Testing2')
        new = Profile.objects.get(id = profile_id)
        self.assertEqual(new.bio, 'Testing2')

    def test_update_project(self):
        self.new_project.save()
        project_id = Projects.objects.last().id
        Projects.update_project_title(project_id, 'Testing2')
        new = Projects.objects.get(id = project_id)
        self.assertEqual(new.title, 'Testing2')

    def test_update_review_design(self):
        self.new_review.save()
        review_id = Review.objects.last().id
        Review.update_review_design(review_id, 2)
        new = Review.objects.get(id = review_id)
        self.assertEqual(new.design, 2)
    
    def test_update_review_usability(self):
        self.new_review.save()
        review_id = Review.objects.last().id
        Review.update_review_usability(review_id, 2)
        new = Review.objects.get(id = review_id)
        self.assertEqual(new.usability, 2)

    def test_update_review_content(self):
        self.new_review.save()
        review_id = Review.objects.last().id
        Review.update_review_content(review_id, 2)
        new = Review.objects.get(id = review_id)
        self.assertEqual(new.content, 2)

    def test_search_by_title(self):
        self.new_project.save()
        project = Projects.search_by_title('Test')
        self.assertTrue(len(project)== 1)
