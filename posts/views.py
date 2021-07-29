from django.contrib.auth import login
from django.shortcuts import render
from .models import Comment, Like,Post
from users.models import Notifications
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse


@login_required
def like_post(request, *args, **kwargs):
    user = request.user
    post_id = request.POST.get("post_id")
    payload = {}
    if request.method=="POST":
        if user.is_authenticated:
            try:
                post = Post.objects.get(pk=post_id)
                try:
                    like = Like.objects.get(user=user, post=post, liked=True)
                    like.liked = False
                    like.save()
                    payload["reponse"] = "Post unliked successfully."
                except Like.DoesNotExist:
                    try:
                        like = Like.objects.get(user=user, post=post, liked=False)
                        like.liked = True
                        like.save()
                        notif = Notifications(user=post.creator,title=f"{user.username} liked your post.")
                        notif.save()
                        payload["reponse"] = "Post liked successfully."
                    except Like.DoesNotExist:
                        like = Like(user=user, post=post, liked=True)
                        like.save()
                        notif = Notifications(user=post.creator,title=f"{user.username} liked your post.")
                        notif.save()
                        payload["reponse"] = "Post liked successfully."

            except Post.DoesNotExist:
                payload["response"] = "This post doesnt seem to exist." 
    else:
        payload["You arent meant to be here this way."]
    return HttpResponse(json.dumps(payload), content_type="application/json")  


def post_view(request, pk):
    my_like = None
    user = request.user
    post = Post.objects.get(pk=pk)
    likes = Like.objects.filter(post=post,liked=True)
    comments = Comment.objects.filter(post=post)
    try:
        mlike = Like.objects.get(user=request.user, post=post, liked=True)
        my_like = True
    except Like.DoesNotExist:
        my_like = False
    is_mine = False
    if post.creator == user:
        is_mine = True
    return render(request,"post.html",{"post":post,"likes":likes,"comments":comments,"my_like":my_like,"is_mine":is_mine})

@login_required
def create_comment(request):
    post_id = request.POST.get("post_id")
    content = request.POST.get("content")
    payload= {}
    user = request.user
    post = Post.objects.get(pk=post_id)
    if request.method == "POST":
        comment = Comment(user=user, post=post, content=content)
        comment.save()


    else:
        payload["You arent meant to be here this way."]
    return HttpResponse(json.dumps(payload), content_type="application/json")  