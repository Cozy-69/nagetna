from django.urls import path
from . import views



app_name = "posts"
urlpatterns = [
    path("like_post/", views.like_post, name="like_post"),
    path("post/<int:pk>", views.post_view, name="post_view"),
    path("create_comment/", views.create_comment, name="create_comment")
]
