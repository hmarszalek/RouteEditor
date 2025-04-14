from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import BackgroundImage, Route, RoutePoint

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .serializers import RouteSerializer, RoutePointSerializer

import json
from django.http import JsonResponse
from django.utils.safestring import mark_safe

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
        return redirect("edit_route", route.id)
    backgrounds = BackgroundImage.objects.all()
    return render(request, "routes/create_route.html", {"backgrounds": backgrounds})

@login_required
def my_routes(request):
    routes = Route.objects.filter(user=request.user)
    return render(request, 'routes/my_routes.html', {'routes': routes})


@login_required
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    points = route.points.all()
    points_data = json.dumps(
        [{"x": p.x, "y": p.y, "name": p.name} for p in points]
    )
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            pointX = data["x"]
            pointY = data["y"]
            point = RoutePoint.objects.create(
                user = request.user,
                route = route,
                name = f"Point {pointX}:{pointY}",
                x = pointX,
                y = pointY
            )
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return render(request, "routes/edit_route.html", {"route": route, "points": points, "points_json": mark_safe(points_data)})

@login_required
def remove_route(request, route_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    route.delete()
    return redirect('my_routes')

@login_required
def remove_point(request, route_id, point_id):
    route = get_object_or_404(Route, id=route_id, user=request.user)
    point = get_object_or_404(RoutePoint, id=point_id, route=route)
    point.delete()
    return redirect('edit_route', route_id=route.id)

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Route.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['delete'])
    def delete_route(self, request, pk=None):
        route = self.get_object()
        route.delete()
        return Response({"message": "Route deleted successfully."})
        
class RoutePointViewSet(viewsets.ModelViewSet):
    serializer_class = RoutePointSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        route_id = self.kwargs.get('route_pk')
        return RoutePoint.objects.filter(user=self.request.user, route_id=route_id)

    def perform_create(self, serializer):
        route_id = self.kwargs.get('route_pk')
        route = get_object_or_404(Route, id=route_id, user=self.request.user)
        serializer.save(user=self.request.user, route=route)