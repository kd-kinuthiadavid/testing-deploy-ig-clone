from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
import datetime as dt

from friendship.exceptions import AlreadyExistsError

from .models import Image, Comment, Profile
from .forms import NewImageForm, NewProfileForm, CommentForm
from friendship.models import Follow


# Create your views here.


def welcome(request):
    title = 'Welcome'
    return render(request, 'welcome.html', {'title': title})

@login_required(login_url='/accounts/login/')
def all_images(request):
    date = dt.date.today()
    images = Image.get_all()
    stories = Profile.objects.all()
    comments = Comment.get_comments()
    return render(request, 'index.html', locals())


@login_required(login_url='/accounts/login/')
def my_profile(request, profile_id):
    date = dt.date.today()
    profile = Profile.objects.filter(user_id=profile_id).first()
    # users = User.objects.get(id=user_id)
    followers = len(Follow.objects.followers(profile.user))
    following = len(Follow.objects.following(profile.user))
    images = Image.objects.filter(user_id=request.user.id)
    print("working")
    return render(request, 'profile.html', locals())

def all_profiles(request):



    return render(request, 'find_friends.html', locals())


def single_profile(request, id):
    profiles = Profile.objects.get(id=id)
    images = Image.objects.filter(user_id=request.user.id)
    users = User.objects.get(id=id)
    followers = len(Follow.objects.followers(users))
    following = len(Follow.objects.following(users))
    return render(request, 'single_profile.html', locals())



def follow(request, profile_id):
    profile = Profile.objects.filter(user_id=profile_id).first()
    try:
        folllow = Follow.objects.add_follower(request.user, profile)
    except AlreadyExistsError:
        return Http404
    print("followed")
    return redirect('/my_profile/' + profile_id)


# @login_required(login_url='/accounts/login/')
# def follow(request,user_id):
#     users = User.objects.get(id=user_id)
#     try:
#         follow = Follow.objects.add_follower(request.user, users)
#     except AlreadyExistsError:
#         return Http404
#     # print("followed")
#     return redirect('/showprofile/'+user_id)

def follow(request, user_id):
    users = User.objects.get(id=user_id)
    try:
        follow = Follow.objects.add_follower(request.user, users)
    except AlreadyExistsError:
        return Http404
    print("why always me?")
    return redirect('/explore/' + user_id)


# @login_required(login_url='/accounts/login/')
# def showprofile(request, user_id):
#     users = User.objects.get(id=user_id)
#     profile = Profile.objects.get(user=users)
#     followers = len(Follow.objects.followers(users))
#     following = len(Follow.objects.following(users))
#     images = Image.objects.filter(author=users)
#     print("showing")
#     return render(request, 'profile/profile.html',{"profile":users,"user":profile,"followers":followers,"following":following,"follow":follow,"images":images})

def explore(request):
    date = dt.date.today()
    profiles = Profile.objects.all()
    return render(request, 'explore.html', locals())


def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
            return redirect('welcome')

    else:
        form = NewImageForm()
    return render(request, 'new_image.html', {"form": form})


def new_profile(request):
    current_user = request.user

    if request.method == 'POST':
        form = NewProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('welcome')
    else:
        form = NewProfileForm()
    return render(request, 'new_profile.html', {"form": form})



def comment(request,image_id):
    try:
        image = Image.objects.get(id = image_id)
    except DoesNotExist:
        raise Http404()

    current_user = request.user
    image_id = image_id
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            com = form.save(commit=False)
            com.by = current_user
            com.image = image
            com.save()
            return redirect('welcome')

    else:
        form = CommentForm()


    return render(request,"comment.html", locals())


def comment_per_image(request, id ):
    comments = Comment.objects.get(id=id)
    return render(request, 'index.html', locals())



def search_results(request):
    if 'instagram' in request.GET and request.GET["instagram"]:
        search_term = request.GET.get("instagram")
        searched_instagrams= Image.search_by_image_caption(search_term)
        message = f"{search_term}"

        return render(request, 'search.html', {"message": message, "images": searched_instagrams})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html', {"message": message})
