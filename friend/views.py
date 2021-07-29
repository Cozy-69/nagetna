from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import json
from users.models import Account, Notifications
from .models import FriendList, FriendRequest

@login_required
def senf_friend_request(request):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = Account.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                    friend_requests = FriendRequest(sender=user, receiver = receiver)
                    notification = Notifications(user=receiver, title=f"New friend request from {user.username}.")
                    notification.save()  
                    friend_requests.save()
                    payload["response"] = "Friend request sent."
                except Exception as e:
                    payload["response"] = str(e)

            except FriendRequest.DoesNotExist:
                friend_requests = FriendRequest(sender=user, receiver=receiver)
                friend_requests.save()
                payload["response"] = "Friend request sent."
            if payload["response"] == None:
                payload["response"] = "Something went wrong."
        else:
            payload["response"] = "Unable to send friend request."        
    else:
        payload["reponse"] = "You must be authenticated to send a friend request."    
    return HttpResponse(json.dumps(payload), content_type="application/json")  

@login_required
def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET" and user.is_authenticated:
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(sender=Account.objects.get(pk=friend_request_id), receiver=user, is_active=True)
            if friend_request.receiver == user:
                if friend_request:
                    friend_request.accept()
                    friend_request.is_active = False
                    friend_request.save()
                    notification = Notifications(user=Account.objects.get(pk=friend_request_id), title=f"{user.username} accepted your Friend request.")
                    notification.save()
                    
                    payload["response"] = "Friend request accepted."
                else:
                    payload["response"] = "Something went wrong."
            else:
                payload["response"] = "That is not your request."
        else:
            payload["response"] = "Unable to accept friend request."
    else:
        payload["response"] = "You must be authenticated to accept a friend request."
    return HttpResponse(json.dumps(payload),content_type="application/json")

@login_required
def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST" and user.is_authenticated:
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            try:
                removee = Account.objects.get(pk=user_id)
                friend_list = FriendList.objects.get(user=user)
                friend_list.unfriend(removee)
                friend_request =  FriendRequest.objects.get(sender=user, receiver=removee)
                friend_request.delete()
                friend_request.save()
                friend_request =  FriendRequest.objects.get(sender=removee, receiver=user)
                friend_request.delete()
                friend_request.save()
                payload["response"] = "Successfully removed frieennd."
            except Exception as e:
                payload["response"] = f"Something went wrong: {str(e)}"
        else:
            payload["response"] = "Unable to remove friend."
    else:
        payload["response"] = "You are not supposed to reach this url like this."
    return HttpResponse(json.dumps(payload), content_type="appliocation/json")


@login_required
def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method=="POST" and user.is_authenticated:
        user_id = request.POST.get("user_id")
        friend_request_id = request.POST.get("friend_request_id")
        if user_id and friend_request_id:
            friend_request = FriendRequest.objects.get(id=friend_request_id ,sender=Account.objects.get(pk=user_id), receiver=user)
            friend_request.decline()
            payload["response"] = "Successfully declined friend request."
        else:
            payload["response"] = "Unable to  cancele/decline friend request."
    else:
        payload["response"] = "You are not supposed to reach this url like this."
    return HttpResponse(json.dumps(payload), content_type="appliocation/json")


def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method=="POST" and user.is_authenticated:
        user_id = request.POST.get("user_id")
        friend_request_id = request.POST.get("friend_request_id")
        if user_id and friend_request_id:
            friend_request = FriendRequest.objects.get(id=friend_request_id, sender=user, receiver=Account.objects.get(pk=user_id))
            friend_request.decline()
            payload["response"] = "Successfully declined friend request."
        else:
            payload["response"] = "Unable to  cancele/decline friend request."
    else:
        payload["response"] = "You are not supposed to reach this url like this."
    return HttpResponse(json.dumps(payload), content_type="appliocation/json")
    