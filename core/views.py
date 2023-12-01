from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.models import User

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout

from .models import Profile,ThreadsContent , LikesFor_Main_Post, FollowersManager, Replies, Likes_for_Replies
from .forms import CreateUserForm, ThreadsContentForm, ProfileForm

from django.contrib.auth.decorators import login_required
from django.db.models import Count

import random
import os

# AUTHENTIOCATION AND AUTHORIZATIONS -------------------------------------------------------------AUTHENTIOCATION AND AUTHORIZATIONS-----------------------------------------------------------
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')

            url = reverse('core:createProfile', kwargs={'user':user})
            return redirect(url)

    context = {'form':form}

    return render(request, 'core/register.html', context)

def createProfile(request, user):

    if request.method == "POST":
        user = User.objects.get(username=user)
        profile_picture = request.FILES.get('profile_picture')
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        profile = Profile(user=user, bio=bio, profile_picture=profile_picture, location=location)
        profile.save()
        messages.success(request, f'Account was created for {user}')

        return redirect('core:login')

    return render(request, 'core/createProfile.html')

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

        else:
            messages.info(request, 'username OR password is incorrect')
            return render(request, 'core/login.html')

    context = {}
    return render(request, 'core/login.html', context)   

def logoutUser(request):
    logout(request)
    return redirect('core:login')


# HOME -------------------------------------------------------------------------------------HOME-----------------------------------



@login_required(login_url='core:login')
def index(request):
    # Getting the current user's profile
    user = request.user
    profile = Profile.objects.get(user=user)

    # Fetch profiles of users followed by the current user using the FollowersManager model
    followed_users = FollowersManager.objects.filter(follower=profile).values_list('followed', flat=True)

    # Fetch posts from the followed users
    followed_posts = ThreadsContent.objects.filter(user__in=followed_users)[:5]

    # Fetch a random set of 10 posts from the database
    random_posts = ThreadsContent.objects.exclude(user__in=followed_users).order_by('?')[:10]

    # Combine followed posts with random posts
    posts = list(followed_posts) + list(random_posts)

    # Shuffle the combined list of posts
    random.shuffle(posts)

    # Getting current user's profile picture
    profImg = profile.profile_picture.url

    # Getting all the posts liked by the current user
    liking = LikesFor_Main_Post.objects.filter(user=profile).values_list('tweet', flat=True)

    # Getting the like counts for each post to be displayed frontend
    like_counts = (
        LikesFor_Main_Post.objects.filter(tweet__in=posts)
        .values('tweet')
        .annotate(like_count=Count('id'))
    )

    # Create a dictionary to store the like counts for each post
    like_counts_dict = {item['tweet']: item['like_count'] for item in like_counts}

    context = {
        'posts': posts[:15],
        'liking': liking,
        'like_counts': like_counts_dict,
        'currentUserProfImg': profImg
    }

    return render(request, 'core/index.html', context)



# Getting owner username of the clicked home option btn
@login_required(login_url='core:login') 
def HomeOptions(request, pk):
    
    #getting all the posts in the data base
    posts = ThreadsContent.objects.all()

    # list that passes a dictionaty carrying the information about the owner of the post
    listdata = []
    for post in posts:
        if post.id == pk:
            listdata.append({'owner':post.user.user.username})
            listdata.append({'ownerId':post.user.user.id})
            print(post.user.user.username)
    
    #postAtrs = list(ThreadsContent.objects.values())


    #data = list(ThreadsContent.objects.filter(id=pk))

    return JsonResponse(listdata, safe=False)


# CRUD OPERATIONS -------------------------------------------------------------------------CRUD OPERATIONS-----------------------------------------------
@login_required(login_url='core:login')
def createPost(request):
    creator = request.user
    creator_Prof = Profile.objects.get(user=creator)
    context = {'posterProf' : creator_Prof}

    if request.method == 'POST':
        content = request.POST.get('content')
        content_img = request.FILES.get('contentImage')

        if content and content_img:
            post = ThreadsContent(content=content, content_img=content_img, user=creator_Prof)
            post.save()
            return JsonResponse({'message':'Upload successful.'})

        if content or content_img:
            if content:
                post = ThreadsContent(content=content, user=creator_Prof)
                post.save()
                return JsonResponse({'message':'Upload successful.'})

            elif content_img:
                post = ThreadsContent(content_img=content_img, user=creator_Prof)                
                post.save()
                return JsonResponse({'message':'Upload successful.'})
        else:
            return JsonResponse({'message':'Title and image are required.'})

    return render(request, 'core/createPost.html', context)

@login_required(login_url='core:login')
def delete_post(request, post_id):
    post = ThreadsContent.objects.get(id=post_id)

    if request.method == 'POST':
        post.delete()
        return JsonResponse({'message':'Post deleted successfully'})

    return JsonResponse({'message':'An error'})

# PROFILE USER -------------------------------------------------------------------------------PROFILE USER-----------------------------------------
@login_required(login_url='core:login')
def Editprofile(request):
    user = request.user  # Assuming the user is authenticated

    # Retrieve the user's profile data
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        # Handle form submission

        old_profile_picture = profile.profile_picture
        if old_profile_picture:
                file_path = old_profile_picture.path
                os.remove(file_path)            

        profile_picture = request.FILES.get('profile_picture')
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        # Update the existing profile data
        profile.user = user
        profile.profile_picture = profile_picture
        profile.bio = bio
        profile.location = location
        profile.save()

        url = reverse('core:posterprofile', kwargs={'pk':user.id})

        return redirect(url)  # Redirect to the profile view page
    else:
        # Pre-fill the form with the existing data
        initial_data = {'profile_picture':profile.profile_picture.url, 'bio': profile.bio, 'location': profile.location}
    
    return render(request, 'core/editProfile.html', {'initial_data': initial_data})
# ---------------------------------------------------------------------------------------------------------------------------------- POSTER PROFILE ------------------
# viewing a post owner profile
@login_required(login_url='core:login')
def posterProfile(request, pk):
    current_user = request.user.id 
    current_user_profile = Profile.objects.get(user=current_user)

    poster = Profile.objects.get(user=pk)

    is_Following = FollowersManager.objects.filter(follower=current_user_profile, followed=poster).exists()

    poster_owned_posts = ThreadsContent.objects.filter(user=poster.id)

    # Counting the user posts by filtering them and counting.
    poster_owned_posts_count = ThreadsContent.objects.filter(user=poster.id).count()

    # counting likes for each post
    like_counts = {}
    for post in poster_owned_posts:
        like_count = LikesFor_Main_Post.objects.filter(tweet=post).count()
        like_counts[post.id] = like_count        

    # counting comments/replies for each post
    comment_counts = {}
    for pst in poster_owned_posts:
        comment_count = Replies.objects.filter(thread=pst).count()
        comment_counts[pst.id] = comment_count

    # counting all instances where given user is being followed
    followersCount = FollowersManager.objects.filter(followed=poster).count()
    # counting all instances where given user is following someone
    followingCount = FollowersManager.objects.filter(follower=poster).count()

    liking = LikesFor_Main_Post.objects.filter(user=current_user_profile).values_list('tweet', flat=True)

    # getting current user's profile picture
    user = request.user.id
    profile = Profile.objects.get(user=user)
    profImg = profile.profile_picture.url

    context = {
        'poster': poster,
        'posts':poster_owned_posts,
        'is_Following':is_Following,
        'followersCount':followersCount,
        'followingCount':followingCount,
        'like_counts' : like_counts,
        'comment_counts': comment_counts,
        'liking': liking,
        'userPostsCount': poster_owned_posts_count,
        'currentUserProfImg':profImg
        }
        
    return render(request, 'core/posterProfile.html', context)


@login_required(login_url='core:login')
def ImageFullView(request, post_id, poster):

    post = ThreadsContent.objects.get(id=post_id, user=poster)

    PostImage = post.content_img.url
    print(PostImage)

    return render(request, 'core/ImageFullView.html', {'PostImage':PostImage})


@login_required(login_url='core:login')
def ImageFullViewHome(request, post_id):

    post = ThreadsContent.objects.get(id=post_id)

    PostImage = post.content_img.url
    print(PostImage)

    return render(request, 'core/ImageFullView.html', {'PostImage':PostImage})


# Likes and follows ---------------------------------------------------------------------------Likes and follows-----------------------------------------
@login_required(login_url='core:login')
def like_post(request, pk):
    user = request.user.id
    profile = Profile.objects.get(user=user)
    tweet = ThreadsContent.objects.get(id=pk)

    liking = LikesFor_Main_Post.objects.filter(user=profile, tweet=pk)

    if liking.exists():
        liking.delete()
        is_liking = False
        # print('unliked')
    else:
        new_like = LikesFor_Main_Post(user=profile, tweet=tweet, value=True)
        new_like.save()
        is_liking = True
        # print('liked')

    likesCount = LikesFor_Main_Post.objects.filter(tweet=pk).count()
    
    return JsonResponse({'likes': likesCount, 'is_liking':is_liking})


# Follow or unfollow                                                ------------------------------------- Following ------------------------
@login_required(login_url='core:login')
def follow_or_unfollow(request, prof_id):
    user = request.user.id 
    profile = Profile.objects.get(user=user)

    user_to_follow = Profile.objects.get(id=prof_id)

    is_following = FollowersManager.objects.filter(follower=profile, followed=user_to_follow).exists()

    if is_following:
        # if already following, unfollow
        FollowersManager.objects.filter(follower=profile, followed=user_to_follow).delete()
        is_following = False
    else:
        # if not following, follow
        FollowersManager.objects.create(follower=profile, followed=user_to_follow)
        is_following = True

    # counting all instances where given user is being followed
    followersCount = FollowersManager.objects.filter(followed=user_to_follow).count()
    # counting all instances where given user is following someone
    followingCount = FollowersManager.objects.filter(follower=user_to_follow).count()
    

    data = {
        'followersCount': followersCount,
        'followingCount': followingCount,
        'is_Following': is_following
    }

    return JsonResponse(data)

# function for following users displayed from a specific account's following or followers
@login_required(login_url='core:login')
def massfollow(request, prof_id):
    user = request.user.id 
    profile = Profile.objects.get(user=user)

    to_follow = User.objects.get(id=prof_id)

    user_to_follow = Profile.objects.get(user=to_follow)

    is_following = FollowersManager.objects.filter(follower=profile, followed=user_to_follow).exists()

    if is_following:
        # if already following, unfollow
        FollowersManager.objects.filter(follower=profile, followed=user_to_follow).delete()
        is_following = False
    else:
        # if not following, follow
        FollowersManager.objects.create(follower=profile, followed=user_to_follow)
        is_following = True

    data = {
       'is_Following': is_following 
    }    

    return JsonResponse(data)

@login_required(login_url='core:login')
def following_view_page(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    currentProf = Profile.objects.get(user=request.user)

        # Retriving every account that is followed by the requested account
    following_byUser = FollowersManager.objects.filter(follower=profile)

        # Retriving everyone that is followed by the current user

    following = FollowersManager.objects.filter(follower=currentProf).values_list('followed', flat=True)

    context = {'user':profile, 'following_byUser':following_byUser, 'following':following}

    return render(request, 'core/following.html', context)

@login_required(login_url='core:login')
def followers_view_page(request, user_id):
    user = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=user)
    currentProf = Profile.objects.get(user=request.user)

        # Retriving every account that follows the requested account
    followers = FollowersManager.objects.filter(followed=profile)

        # Retriving everyone that is followed by the current user
    following = FollowersManager.objects.filter(follower=currentProf).values_list('followed', flat=True)


    context = {'user':profile, 'followers':followers, 'following':following}

    return render(request, 'core/followers.html', context)

# ----------------------------------------- Replies ---------------------------
@login_required(login_url='core:login')
def main_replies(request, post_id):
    user = request.user.id 
    profile = Profile.objects.get(user=user)

    # getting the post passed by the url
    post = ThreadsContent.objects.get(id=post_id)

    # getting all posts associated with the post
    replies = Replies.objects.filter(thread=post)
    repliesLength = Replies.objects.filter(thread=post).count()

    # list to be passed as Json Response after the for loop operation
    listdata = []
    for reply in replies:
        reply_likes_count = Likes_for_Replies.objects.filter(likeFor=reply).count()
        currentUserLikedThisPost = Likes_for_Replies.objects.filter(user=profile, likeFor=reply).exists()

        dictdata = {
            'replyid': reply.id,
            'reply' : reply.reply,
            'author' : reply.user.user.username,
            'authorProfile' : reply.user.profile_picture.url,
            'date': reply.timestamp,
            'replyLikesCount': reply_likes_count,
            'currentUserLikedThisPost' : currentUserLikedThisPost,
        }
        listdata.append(dictdata)

    return JsonResponse({'replies':listdata})

   # Sending replies to targeted posts
@login_required(login_url='core:login')
def sendReply(request, post_id):
    user = request.user

    profile = Profile.objects.get(user=user)

    thread = ThreadsContent.objects.get(id=post_id)

    if request.method == 'POST':
        content = request.POST.get('replyText')
        
        
        if content :
            reply = Replies(reply=content, user=profile, thread=thread)
            reply.save()

            replycounts = Replies.objects.filter(thread=thread).count()

            return JsonResponse({'replycounts':replycounts})
        else:
            return JsonResponse({'responseMsg': "Can't upload bank reply"})

    # Liking a reply
@login_required(login_url='core:login')
def likeReply(request, reply_id):
    user = request.user
    profile = Profile.objects.get(user=user)
    beingLiked = Replies.objects.get(id=reply_id)

    doesUserLikeThisReplyAlready = Likes_for_Replies.objects.filter(user=profile,likeFor=beingLiked).exists()
    if doesUserLikeThisReplyAlready == False:
        like = Likes_for_Replies(user=profile, value=True, likeFor=beingLiked)
        like.save()
    else:
        Likes_for_Replies.objects.filter(user=profile,likeFor=beingLiked).delete()

    likesForThisReplyCount = Likes_for_Replies.objects.filter(likeFor=beingLiked).count()
    userlikedThis = Likes_for_Replies.objects.filter(user=profile,likeFor=beingLiked).exists()
    return JsonResponse({'likesForThisReplyCount': likesForThisReplyCount, 'userlikedThis':userlikedThis})