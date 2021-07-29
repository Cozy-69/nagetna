from friend.models import FriendList
from posts.models import Comment, Post, Like
from django.shortcuts import redirect, render
from posts.forms import PostCreationForm
from django.contrib import messages


def homepage(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = PostCreationForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                creator = request.user
                obj.creator = creator
                obj.save()
                messages.success((request), "Post has been create successfully.")
                return redirect("homepage")
            else:
                messages.success((request), "Form was not valid.")
                return redirect("homepage")
        else:
            messages.info((request), "You have to be logged in to create a post.")
            return redirect("homepage")
    else:
        if request.user.is_authenticated:
            posts = Post.objects.all()
            try:
                friends = FriendList.objects.get(user=request.user).friends.all()
                final_posts = []

                for post in posts:
                    if post.creator in friends:
                        post_comments = Comment.objects.filter(post=post)
                        try:
                            mylike = Like.objects.get(user=request.user, post=post, liked=True)
                            likes = Like.objects.filter(post=post, liked=True)
                            final_posts.append((post,likes,True,post_comments))
                        except Like.DoesNotExist:
                            likes = Like.objects.filter(post=post, liked=True)
                            final_posts.append((post,likes,False,post_comments))
                return render(request, "home.html",{"posts": final_posts})
            except FriendList.DoesNotExist:
                return render(request, "home.html")
            
        else:
            return render(request, "home.html")

def about(request):
    return render(request, "about.html")
