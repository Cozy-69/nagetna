from django.contrib import admin

from .models import FriendRequest,FriendList


admin.site.register([FriendRequest, FriendList])
