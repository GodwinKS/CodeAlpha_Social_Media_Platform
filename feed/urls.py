from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_list, name='feed_list'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # NEW: Profile and Follow Routes
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<int:pk>/', views.follow_unfollow, name='follow_unfollow'),
]