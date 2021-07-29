from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "chat"
urlpatterns = [
    path("chat/<int:pk>/", views.chatroom, name="chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
]
