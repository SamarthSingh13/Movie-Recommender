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
from .tmdbapi import get_img_url
num_movies = 20
num_users = 10
num_display = 20 # Only half are displayeed
# Create your views here.

def subset(shows):
    return [show for show in shows if show.poster_url != ""][:num_display//2] if shows else None

def index(request):
    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)[0:num_display]

        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes[0:num_display]
    top_movies = Show.top_movies(0, num_display)
    if request.user.is_authenticated:
        user = request.user
        user = UserProfile.nodes.get(username=user.username)
        rec_movies = user.recommendations(num_movies, num_users)
    else:
        rec_movies = None
    for show_set in [shows, top_movies, rec_movies]:
        if show_set is None:
            continue
        for show in show_set:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
    return render(request, 'home.html', {'shows': subset(shows), 'top_movies': subset(top_movies), 'rec_movies':subset(rec_movies)})

# Show the search result
def search(request):
    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)[0:num_display]
        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes[0:num_display]
    top_movies = Show.top_movies(0, num_display)
    for show_set in [shows, top_movies]:
        if show_set is None:
            continue
        for show in show_set:
            show.poster_url = get_img_url(show.title)
            show.save()
    return render(request, 'home.html', {'shows': subset(shows),'top_movies': subset(top_movies)})


# Show details of the movie
def detail(request, movie_id):

    # if not request.user.is_active:
    #     raise Http404
    # movie = Show.nodes.get_or_none(_id=movie_id)
    movie = Show.get_by_id(movie_id)
    if movie is None:
        raise Http404


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

    # temp = list(MyList.objects.all().values().filter(movie_id=movie_id,user=request.user))
    # if temp:
    #     update = temp[0]['watch']
    # else:
    #     update = False
    update = False
    if request.method == "POST":

        # For my list
        # if 'watch' in request.POST:
        #     watch_flag = request.POST['watch']
        #     if watch_flag == 'on':
        #         update = True
        #     else:
        #         update = False
        #     if MyList.objects.all().values().filter(movie_id=movie_id,user=request.user):
        #         MyList.objects.all().values().filter(movie_id=movie_id,user=request.user).update(watch=update)
        #     else:
        #         q=MyList(user=request.user,movie=movie,watch=update)
        #         q.save()
        #     if update:
        #         messages.success(request, "Show added to your list!")
        #     else:
        #         messages.success(request, "Show removed from your list!")
        #
        #
        # # For rating
        # else:
        rate = request.POST['rating']
        if request.user.is_authenticated:
            user = request.user
            user = UserProfile.nodes.get(username=user.username)
        if user.ratings.is_connected(movie):
            r = user.ratings.relationship(movie)
            r.numeic = rate
        else:
            r = user.ratings.connect(movie, {'numeric': rate})
            r.save()
            user.save()
        # if Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user):
        #     Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user).update(rating=rate)
        # else:
        #     q=Myrating(user=request.user,movie=movie,rating=rate)
        #     q.save()

        # messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    rate_flag = False
    movie_rating = 0
    if request.user.is_authenticated:
        user = UserProfile.nodes.get(username=request.user.username)
        rate_flag = user.ratings.is_connected(movie)


        if rate_flag:
            movie_rating = user.ratings.relationship(movie).numeric
    # out = list(Myrating.objects.filter(user=request.user.id).values())
    #
    # # To display ratings in the movie detail page
    # movie_rating = 0
    # rate_flag = False
    # for each in out:
    #     if each['movie_id'] == movie_id:
    #         movie_rating = each['rating']
    #         rate_flag = True
    #         break

    context = {'movies': movie,'movie_rating':movie_rating,'rate_flag':rate_flag,'update':update,
               'genre':movie.get_my_genre(), 'director':movie.get_my_director(), 'actors': movie.get_my_actor(),
               'language': movie.get_my_language(), 'ott': movie.get_my_ott(), 'country': movie.get_my_country()}
    return render(request, 'detail.html', context)



# TV shows/ Shows functionality
def tv_shows(request):


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)[0:num_display]

        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes[0:num_display]
    return render(request, 'mtv.html', {'shows': subset(shows)})

def movies(request):


    query = request.GET.get('q')

    if query:
        if request.GET.get('search_query'):
            shows = Show.nodes.filter(title__icontains=query)[0:num_display]
            header = 'Search Result'
        else:
            shows = Show.get_genre(query, 0, num_display)
            header = query + ' Movies'
        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': subset(shows), 'header': header})


    shows = Show.nodes[0:num_display]
    thriller_shows = Show.get_genre("Thriller", 0, num_display)
    comedy_shows = Show.get_genre("Comedy", 0, num_display)
    romance_shows = Show.get_genre("Romance", 0, num_display)
    action_shows = Show.get_genre("Action", 0, num_display)
    scifi_shows = Show.get_genre("Sci-Fi", 0, num_display)
    for show_set in [shows, thriller_shows, comedy_shows, romance_shows, action_shows, scifi_shows]:
        for show in show_set:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()

    return render(request, 'mtv.html', {'shows': subset(shows),'thriller': subset(thriller_shows), 'comedy': subset(comedy_shows), 'romance': subset(romance_shows), 'action': subset(action_shows), 'scifi': subset(scifi_shows)})

# recently added functionality
def recently_added(request):


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)[0:num_display]

        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': shows})

    shows = Show.nodes[0:num_display]
    return render(request, 'recently_added.html', {'shows': subset(shows)})

# MyList functionality
def mylist(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404


    query = request.GET.get('q')

    if query:
        movies = Show.nodes.filter(title__icontains=query)

        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
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
    return Http404
