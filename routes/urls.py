from django.urls import path
from . import views
from .views import home, register_view, login_view, logout_view, create_route

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('create_route/', create_route, name='create_route'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)