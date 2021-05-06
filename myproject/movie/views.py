from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.http import Http404
from .models import Ott, Genre, Language, Country, Show, UserProfile
from .models import Rating, Person #Mru
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Case, When
import pandas as pd

# Create your views here.
def index(request):
    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query).distinct()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes.all()
    return render(request, 'home.html', {'shows': shows})

# Show the search result
def search(request):
    shows = Show.objects.all()
    query = request.GET.get('q')

    if query:
        shows = Show.objects.filter(title__icontains=query).distinct()
        return render(request, 'search.html', {'shows': shows})

    return render(request, 'home.html', {'shows': shows})

# Show details of the movie
def detail(request, movie_id):

    if not request.user.is_active:
        raise Http404
    movies = get_object_or_404(Show, id=movie_id)
    movie = Show.objects.get(id=movie_id)

    temp = list(MyList.objects.all().values().filter(movie_id=movie_id,user=request.user))
    if temp:
        update = temp[0]['watch']
    else:
        update = False
    if request.method == "POST":

        # For my list
        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            if watch_flag == 'on':
                update = True
            else:
                update = False
            if MyList.objects.all().values().filter(movie_id=movie_id,user=request.user):
                MyList.objects.all().values().filter(movie_id=movie_id,user=request.user).update(watch=update)
            else:
                q=MyList(user=request.user,movie=movie,watch=update)
                q.save()
            if update:
                messages.success(request, "Show added to your list!")
            else:
                messages.success(request, "Show removed from your list!")


        # For rating
        else:
            rate = request.POST['rating']
            if Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user):
                Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user).update(rating=rate)
            else:
                q=Myrating(user=request.user,movie=movie,rating=rate)
                q.save()

            messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    out = list(Myrating.objects.filter(user=request.user.id).values())

    # To display ratings in the movie detail page
    movie_rating = 0
    rate_flag = False
    for each in out:
        if each['movie_id'] == movie_id:
            movie_rating = each['rating']
            rate_flag = True
            break

    context = {'movies': movies,'movie_rating':movie_rating,'rate_flag':rate_flag,'update':update}
    return render(request, 'detail.html', context)



# TV shows/ Shows functionality
def tv_shows(request):


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query).distinct()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes.all()
    return render(request, 'mtv.html', {'shows': shows})

def movies(request):


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query).distinct()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes.all()
    return render(request, 'mtv.html', {'shows': shows})

# recently added functionality
def recently_added(request):


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query).distinct()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes.all()
    return render(request, 'recently_added.html', {'shows': shows})

# MyList functionality
def mylist(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404


    query = request.GET.get('q')

    if query:
        movies = Show.nodes.filter(title__icontains=query).distinct()
        return render(request, 'mylist.html', {'movies': movies})

    movies = Show.nodes.filter(mylist__watch=True,mylist__user=request.user)
    return render(request, 'mylist.html', {'movies': movies})


# Register user
def signUp(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")

    context = {'form': form}

    return render(request, 'signup.html', context)


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'login.html', {'error_message': 'Your account disabled'})
        else:
            return render(request, 'login.html', {'error_message': 'Invalid Login'})

    return render(request, 'login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")

# My profile
def account(request):
    shows = Show.nodes.all()
    return render(request, 'home.html', {'shows': shows})
