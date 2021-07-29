from django.urls import path
from . import views


app_name = "friend"

urlpatterns = [
    path("friend_request/", views.senf_friend_request, name="friend-request"),
    path("friend_request/decline/", views.decline_friend_request, name="friend-request-decline"),
    path("friend_request/cancel/", views.cancel_friend_request, name="friend-request-cancel"),
    path("accept_friend_request/<friend_request_id>", views.accept_friend_request, name="friend-request-accept"),
    path("friend_remove/", views.remove_friend, name="remove-friend"),
]
