from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import BackgroundImage, Route, RoutePoint

def home(request):
    return render(request, "routes/home.html")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "routes/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "routes/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def create_route(request):
    if request.method == 'POST':
        background_id = request.POST.get("background")
        background = BackgroundImage.objects.get(id=background_id)
        route_name = request.POST.get("name")
        route = Route.objects.create(user=request.user, name=route_name, background=background)
        return redirect("home")
    backgrounds = BackgroundImage.objects.all()
    return render(request, "routes/create_route.html", {"backgrounds": backgrounds})