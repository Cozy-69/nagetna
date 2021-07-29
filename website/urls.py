from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("users.urls")),
    path('', include("posts.urls")),
    path('', include("chat.urls")),
    path("friend/", include("friend.urls")),
    path('', views.homepage,name="homepage"),
    path('about/', views.about,name="about"),
]
