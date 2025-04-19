from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['full_name'].split()[0],
                last_name=form.cleaned_data['full_name'].split()[1],
                email=form.cleaned_data['email']
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('create_request')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def create_request(request):
    form = RequestForm()

    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            
            if form.cleaned_data['other_service']:
                request_instance.other_service_description = form.cleaned_data['other_service_description']
            else:
                request_instance.service = form.cleaned_data['service']
            
            request_instance.save()
            return redirect('request_history')

    services = Service.objects.all()
    return render(request, 'create_request.html', {'form': form, 'services': services})

@login_required
def request_history(request):
    requests = Request.objects.filter(user=request.user)
    return render(request, 'request_history.html', {'requests': requests})

@login_required
def logout_view(request):
    logout(request)
    return redirect('register')

def robots_txt(request):
    lines = ["User-agent: *","Allow: /", "Allow: /request_history/", "Disallow: /login/", "Disallow: /register/", "Sitemap: https://127.0.0.1:8000/sitemap.xml"]
    return HttpResponse("\n".join(lines), content_type="text/plain")

class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return ['create_request', 'request_history', 'login', 'register']

    def location(self, item):
        return reverse(item)
   