from django.urls import path
from . import views
from .views import home, register_view, login_view, logout_view, create_route, my_routes, edit_route, remove_route, remove_point

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('create_route/', create_route, name='create_route'),
    path('my_routes/', my_routes, name='my_routes'),
    path('edit_route/<int:route_id>/', edit_route, name='edit_route'),
    path('remove_route/<int:route_id>/', remove_route, name='remove_route'),
    path('remove_point/<int:route_id>/<int:point_id>/', remove_point, name='remove_point'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)