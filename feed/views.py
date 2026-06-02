from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User         # <-- Add User import
from .models import Post, Comment, Profile          # <-- Add Profile import here
from .forms import PostForm, CommentForm

def feed_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user       
            post.save()                    
            return redirect('feed_list')   
            
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')
    comment_form = CommentForm()  # <-- Create an empty comment box to send to the HTML
    
    return render(request, 'feed/index.html', {'posts': posts, 'form': form, 'comment_form': comment_form})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)     
    return redirect('feed_list')

# NEW: Logic for saving a comment
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post           # Link the comment to the specific post
            comment.user = request.user   # Link the comment to the logged-in user
            comment.save()
    return redirect('feed_list')
# NEW: View a User's Profile
def profile(request, username):
    # Find the user, and get or create their profile so it doesn't crash
    user_profile = get_object_or_404(User, username=username)
    target_profile, created = Profile.objects.get_or_create(user=user_profile)
    my_profile, created = Profile.objects.get_or_create(user=request.user)
    
    # Get only the posts written by this specific user
    posts = Post.objects.filter(user=user_profile).order_by('-created_at')
    
    return render(request, 'feed/profile.html', {
        'user_profile': user_profile, 
        'target_profile': target_profile, 
        'my_profile': my_profile, 
        'posts': posts
    })

# NEW: Logic to Follow/Unfollow
def follow_unfollow(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    target_profile, created = Profile.objects.get_or_create(user=target_user)
    my_profile, created = Profile.objects.get_or_create(user=request.user)
    
    # If I am already following them, unfollow. Otherwise, follow.
    if target_profile in my_profile.follows.all():
        my_profile.follows.remove(target_profile)
    else:
        my_profile.follows.add(target_profile)
        
    return redirect('profile', username=target_user.username)