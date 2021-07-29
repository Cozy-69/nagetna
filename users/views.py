from django.conf import settings
from django.contrib.auth.models import User
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AccountRegistrationForm, AccountAuthenticateForm, AccountEditForm
from .models import Account, Notifications
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse 
from friend.utils import get_friend_request_or_false
from django.http import HttpResponse
import json




def account_signup(request):
    user = request.user
    if user.is_authenticated:
        messages.info(request, ("You are already signed in."))
        return redirect("homepage")
    if request.POST:
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your account was create successfully."))
            return redirect('users:login')
        else:
            messages.warning(request, (form.errors))
            return redirect('users:signup')
    else:        
        return render(request, "signup.html")

def account_login(request):
    user = request.user
    if user.is_authenticated:
            messages.info("You are already logged in.")
            return redirect('homepage')
    if request.method == 'POST':
        form = AccountAuthenticateForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, ("You have been logged in successfully."))
                return redirect("homepage")
            else :
                messages.warning(request, ("Please verify your login information."))
                return redirect("users:login")    
        else:
            messages.warning(request, (form.errors))
            return redirect("users:login")  

    else:
        return render(request, "login.html")


def account_logout(request):
    logout(request)
    messages.success(request, ("You have been logged out successfully."))
    return redirect("homepage")



def account_view(request, pk):
    request_sent = 0
    friend_requests = 0
    context = {}
    try:
        account = Account.objects.get(id=pk)
    except Account.DoesNotExist:
        messages.warning(request,("That account seems to not exist in our database."))
        return redirect("homepage")
    if account:
        try:
            friend_list = FriendList.objects.get(user=account)
        except FriendList.DoesNotExist:
            friend_list = FriendList(user=account)
            friend_list.save()
        friends = friend_list.friends.all()
        context["user"] = account
        context["friends"] = friends
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user!=account:
            is_self = False
            if friends.filter(pk=user.id):
                is_friend = True
            else:
                is_friend = False
                if get_friend_request_or_false(sender=account, receiver=user):
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context["pending_friend_request_id"] = get_friend_request_or_false(sender=account, receiver=user).id
                elif get_friend_request_or_false(sender=user, receiver=account) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                    context["pending_friend_request_id"] = get_friend_request_or_false(sender=user, receiver=account).id
                else:
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        elif not user.is_authenticated:
            is_self = False
        else:
            friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)

        context["is_self"] = is_self
        context["notifications"] = Notifications.objects.filter(user=request.user, is_active=True)
        context["is_friend"] = is_friend
        context["request_sent"] = request_sent
        context["friend_requests"] = friend_requests
        return render(request, "account.html", context)
    else:
        messages.warning((request), "Sorry, something went wrong.")
        return redirect("homepage")



def search_view(request, query):
    context = {}
    if request.method=="GET":
        if len(query) > 0:
            search_results = Account.objects.filter(username__icontains=query)
            context["accounts"] = search_results
            

        return render(request, "search_results.html", context)

 
@method_decorator(login_required,name='dispatch')
class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    # form = AccountEditForm
    fields = ["username","email","birth_day","bio","profile_image", "hide_email", "hide_birth_day"]
    template_name = "account_edit.html"
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.get(pk=self.request.user.id)
        return queryset

    def get_success_url(self):
        return reverse("users:account", kwargs={"pk": self.request.user.id})


@login_required
def delete_notification(request, notification_id):
    notification = Notifications.objects.get(user=request.user, id=notification_id)
    notification.is_active = False
    notification.save()
    return redirect(reverse("users:account", kwargs={"pk": request.user.id}))

