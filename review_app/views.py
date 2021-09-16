from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.urls.base import reverse
from .forms import RegistrationForm, ProfileUpdateForm, ReviewForm, ProjectUpdateForm
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Review, Projects
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormMixin
from itertools import chain

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


def search_results(request):  

    if 'search_user' in request.GET and request.GET["search_user"]:
        search_term = request.GET.get("search_user")
        searched_users = Profile.search_by_username(search_term)
        message = f"{search_term}"
        title = search_term
        return render(request, 'others/search_results.html',{"message": message, "users": searched_users, 'title': title})
    else:
        message = "You haven't searched for any term"
        return render(request, 'others/search_results.html',{"message": message})


def logout_view(request):
    logout(request)
    return redirect('login')