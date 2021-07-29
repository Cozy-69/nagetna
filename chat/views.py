import datetime
from chat.models import Message
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.models import Account
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
import json
from django.http import HttpResponse
from users.models import Notifications

# Create your views here.


@login_required
def chatroom(request, pk):
    other_user = Account.objects.get(pk=pk)
    if other_user != request.user:
        messages_chat = Message.objects.filter(Q(receiver=request.user, sender=other_user))
        messages_chat.update(seen=True)
        messages_chat = messages_chat | Message.objects.filter(Q(receiver=other_user, sender=request.user))
        return render(request, "chatroom.html", {"other_user": other_user, "user_messages": messages_chat, "user":request.user})
    else:
        messages.warning((request),"You cant chat with your self")
        return redirect("homepage")

@login_required
def ajax_load_messages(request, pk):
    payload = {}
    other_user = Account.objects.get(pk=pk)
    messages_list = Message.objects.filter(seen=False, receiver=request.user)
    message_list  = [{
        "sender": single_message.sender,
        "content": single_message.content,
        "sent": single_message.sender == request.user,
        "date_created": naturaltime(single_message.date_created),


    } for single_message in messages_list]
    messages_list.update(seen=True)

    if request.method == "POST":
        single_message = request.POST.get("message_contetnt")
        m = Message.objects.create(receiver=other_user, sender=request.user, content=single_message,seen=False)
        Notifications.objects.create(user=other_user, title=f"You have received a new message from {request.user.username}")
        message_list.append({
        "sender": request.user,
        "content": m.content,
        "sent": True,
        "date_created": datetime.datetime.now()
        })
        payload["response"] = "Successfully sent message."
        return HttpResponse(json.dumps(payload),content_type="application/json")
    elif request.method == "GET":
        messages_list = Message.objects.filter(Q(receiver=request.user, sender=other_user, seen=False))
        messages_list = messages_list | Message.objects.filter(Q(receiver=other_user, sender=request.user, seen=False))
        payload["messages_list"] = list(messages_list)
        return HttpResponse(json.dumps(payload),content_type="application/json")

