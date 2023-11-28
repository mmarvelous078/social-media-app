from django.urls import path 
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index , name='index'),

    # ************************************************************************Authentication
    path('register/', views.registerPage , name='register'),
    path('login/', views.loginPage , name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('createProfile/<str:user>', views.createProfile, name="createProfile"),

    # ***********************************************************************Profile
    path('Editprofile/', views.Editprofile, name='Editprofile'),
    path('posterProfile/<int:pk>', views.posterProfile, name='posterprofile'),
    path('followOrunfollow/<int:prof_id>', views.follow_or_unfollow, name='follow_or_unfollow'),

    path('viewfollowing/massfollow/<int:prof_id>', views.massfollow, name='massfollowing'),
    path('viewfollowers/massfollow/<int:prof_id>', views.massfollow, name='massfollower'),

    path('viewfollowing/<int:user_id>', views.following_view_page ,name='viewfollowing'),
    path('viewfollowers/<int:user_id>', views.followers_view_page ,name='viewfollowers'),

    path('ImageFullView/<int:post_id>/<int:poster>', views.ImageFullView, name='ImageFullView'),
    path('ImageFullViewHome/<int:post_id>', views.ImageFullViewHome, name='ImageFullViewHome'),

    #***********************************************************************Posts
    path('createPost/', views.createPost , name='createPost'),
    path('delete_post/<int:post_id>', views.delete_post, name='delete_post'),
    path('likepost/<int:pk>', views.like_post, name='likepost'),

    # ***********************************************************************Comments or Replies
    path('main_replies/<int:post_id>', views.main_replies, name='main_replies'),
    path('posterProfile/main_replies/<int:post_id>', views.main_replies, name='main_replies'),
    path('sendReply/<int:post_id>', views.sendReply, name='sendReply'),
    path('likeReply/<int:reply_id>', views.likeReply, name='likeReply'),
    path('posterProfile/likeReply/<int:reply_id>', views.likeReply, name='likeReply'),

    #***********************************************************************home modal options
    path('home/options/<int:pk>', views.HomeOptions, name='homeoptions')
]
