from django.http.response import Http404
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls.base import reverse
from .forms import RegistrationForm, ProfileUpdateForm, ReviewForm, ProjectForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Review, Projects
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from itertools import chain
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer, ProjectSerializer
from .permissions import IsAdminOrReadOnly
import statistics

# Create your views here.
def register(request):

    rgf = RegistrationForm()

    if request.method == 'POST':
        rgf = RegistrationForm(request.POST)
        if rgf.is_valid():
            rgf.save()
            user = rgf.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    return render(request, 'register.html', {'rgf': rgf})

def loginuser(request):
 
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')

@login_required('')
def HomeView(request):

    projects = Projects.objects.all()
    title = 'Home of Reviews'
    user = request.user

    pf = ProjectForm()

    if request.method == 'POST':
        pf = ProjectForm(request.POST, request.FILES)
        if pf.is_valid():
            post = pf.save(commit = False)
            post.posted_by = user
            post.save()
            return redirect('home')
    else:
        pf = ProjectForm()

    return render (request, 'home.html', {'title': title, 'projects': projects, 'user': user, 'pf': pf})

@login_required('')
def my_profile(request):

    profile = Profile.objects.filter(user = request.user).first()
    projects = Projects.objects.filter(posted_by = request.user.id).all()
    title = f'{ request.user.username }\'s Profile'

    uf = ProfileUpdateForm()
    user = request.user

    if request.method == 'POST':
        uf = ProfileUpdateForm(request.POST, request.FILES)
        if uf.is_valid():
            post = uf.save(commit = False)
            post.user = user
            post.save()
            return redirect('home')
    else:
        uf = ProfileUpdateForm()

    return render (request, 'myprofile.html', {'title': title, 'profile': profile, 'projects': projects, 'uf': uf})

class HomeView2(ListView):
    model = Projects
    template_name = 'home.html'
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Home of Reviews'
        context['title'] = title
        return context 

def project(request, pk):

    project = Projects.objects.filter(pk = pk).first()
    user = project.posted_by
    profile = Profile.objects.filter(user = user).first()

    user2 = request.user
    rf = ReviewForm()

    design = Review.objects.filter(reviewed_project = pk).values_list('design', flat=True)
    usability = Review.objects.filter(reviewed_project = pk).values_list('usability', flat=True)
    content = Review.objects.filter(reviewed_project = pk).values_list('content', flat=True)

    if len(design) > 0 and len(usability) > 0 and len(content) > 0:
        avg_design = round(statistics.mean(design), 1)
        avg_usability = round(statistics.mean(usability), 1)
        avg_content = round(statistics.mean(content), 1)
    else:
        avg_content = 0
        avg_design = 0
        avg_usability = 0

    if request.method == 'POST':
        rf = ReviewForm(request.POST)
        if rf.is_valid():
            review = rf.save(commit = False)
            review.reviewer = user2
            review.reviewed_project = project
            review.save()
            return HttpResponseRedirect(reverse('project', args = [pk]))
        else:
            rf = ReviewForm

    return render(request, 'project.html', {'project': project, 'profile': profile, 'rf': rf, 'design': avg_design, 'usability':avg_usability, 'content': avg_content})

def rate(request, pk):
    project = Projects.objects.filter(pk = pk).first()
    user = request.user
    rf = ReviewForm()

    if request.method == 'POST':
        rf = ReviewForm(request.POST)
        if rf.is_valid():
            review = rf.save(commit = False)
            review.reviewer = user
            review.reviewed_project = project
            review.save()
            return redirect(request.META.get('HTTP_REFERER'))
            # return HttpResponseRedirect(reverse('project', args = [int(pk)]))
        else:
            rf = ReviewForm


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Projects
    template_name = 'project.html'
    context_object_name = 'project'

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'update_profile.html'

class UpdateProjectView(LoginRequiredMixin, UpdateView):
    model = Projects 
    form_class = ProjectForm
    template_name = 'update_project.html'

class DeleteProjectView(LoginRequiredMixin, DeleteView):
    model = Projects
    template_name = 'delete_projects.html'
    success_url = reverse_lazy('home')

class ProjectList(APIView):

    # permission_classes = (IsAdminOrReadOnly, )

    def get_project(self, pk):
        try:
            return Projects.objects.get(pk = pk)
        except Projects.DoesNotExist:
            return Http404

    def get(self, request, format = None):
        all_projects = Projects.objects.all()
        serializers = ProjectSerializer(all_projects, many = True)
        return Response(serializers.data)


    def post(self, request, format = None):
        serializers = ProjectSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

class OneProject(APIView):

    # permission_classes = (IsAdminOrReadOnly, )

    def get_project(self, pk):
        try:
            return Projects.objects.get(pk = pk)
        except Projects.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OneProfile(APIView):

    # permission_classes = (IsAdminOrReadOnly, )

    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk = pk)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, pk, format = None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        profile = self.get_profile(pk)
        serializers = ProfileSerializer(profile, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileList(APIView):

    # permission_classes = (IsAdminOrReadOnly, )

    def get(self, request, format = None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many = True)
        return Response(serializers.data)

    def get_profile(self, pk):
        try:
            return Profile.objects.get(pk = pk)
        except Profile.DoesNotExist:
            return Http404
    
    def post(self, request, format = None):
        serializers = ProfileSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status = status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)
 
@login_required
def search_results(request):  

    if 'search_user' in request.GET and request.GET["search_user"]:
        search_term = request.GET.get("search_user")
        searched_projects = Projects.search_by_title(search_term)
        message = f"{search_term}"
        title = search_term
        return render(request, 'search.html',{"message": message, "projects": searched_projects, 'title': title})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message": message})

def logout_view(request):
    logout(request)
    return redirect('login')