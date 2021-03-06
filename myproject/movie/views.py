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
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
import pandas as pd
from .tmdbapi import get_img_url
num_movies = 20
num_users = 10
num_display = 24 # Only half are displayeed
# Create your views here.

def subset(shows):
    return [show for show in shows if show.poster_url != "" and len(show.title)<=30][:num_display//2] if shows else None

def index(request):
    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)[0:num_display]

        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': subset(shows)})

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
        return render(request, 'search.html', {'shows': subset(shows)})

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



    # temp = list(MyList.objects.all().values().filter(movie_id=movie_id,user=request.user))
    # user = UserProfile.nodes.get(username=user.username)
    # temp =  user.watchlist
    # if temp:
    #     update = temp[0]['watch']
    # else:
    #     update = False
    update = False
    upvoted = False
    downvoted = False
    if request.method == "POST":
        user = request.user
        if user.is_authenticated:
            user = UserProfile.nodes.get(username=user.username)
        else:
            return Http401
        # For my list
        if 'upvote' in request.POST:
            review_id = request.POST['review']
            if user.reviews_voted.is_connected(Rating.get_by_id(review_id)):
                fl = user.reviews_voted.relationship(Rating.get_by_id(review_id))
                if fl.value == -1:
                    fl.value = 1
            else :
                user.reviews_voted.connect(Rating.get_by_id(review_id),{'value':1})
            upvoted = True

        if 'downvote' in request.POST:
            review_id = request.POST['review']
            if user.reviews_voted.is_connected(Rating.get_by_id(review_id)):
                fl = user.reviews_voted.relationship(Rating.get_by_id(review_id))
                if fl.value == 1:
                    fl.value = -1
            else :
                user.reviews_voted.connect(Rating.get_by_id(review_id),{'value':-1})
            downvoted = True

        if 'watch' in request.POST:
            watch_flag = request.POST['watch']
            # print(watch_flag)
            if watch_flag == 'Add to Watchlist':
                if not user.watchlist.is_connected(movie):
                    user.watchlist.connect(movie)

            else:
                if user.watchlist.is_connected(movie):
                    user.watchlist.disconnect(movie)

        # # For rating
        else:
            for k in request.POST:
                print(k, request.POST[k])
            rate = int(float(request.POST['rating']))

            if user.ratings.is_connected(movie):
                r = user.ratings.relationship(movie)
                movie.overall_rating = ((movie.overall_rating*movie.num_votes)+rate-r.numeric)/movie.num_votes
                movie.save()
                r.numeric = rate
                r.review = request.POST['review']
                if r.review == "":
                    r.review = None
                r.save()
                user.save()
            else:
                r = user.ratings.connect(movie, {'numeric': rate, 'review': request.POST['review'] if request.POST['review'] != "" else None})
                movie.num_votes += 1
                if movie.overall_rating is None:
                    movie.overall_rating = rate
                else:
                    movie.overall_rating = ((movie.overall_rating*(movie.num_votes-1))+rate)/movie.num_votes
                movie.save()
                r.save()
            movie.save()
            user.save()
            # if Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user):
            #     Myrating.objects.all().values().filter(movie_id=movie_id,user=request.user).update(rating=rate)
            # else:
            #     q=Myrating(user=request.user,movie=movie,rating=rate)
            #     q.save()

            # messages.success(request, "Rating has been submitted!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    rate_flag = False
    in_watchlist = False
    movie_rating = 0
    movie_review = ''
    if request.user.is_authenticated:
        user = UserProfile.nodes.get(username=request.user.username)
        rate_flag = user.ratings.is_connected(movie)
        in_watchlist = user.watchlist.is_connected(movie)

        if rate_flag:
            movie_rating = user.ratings.relationship(movie).numeric
            movie_review = user.ratings.relationship(movie).review
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
    # print(movie_review)
    # print(movie.reviews())
    context = {'movies': movie,'movie_rating':movie_rating,'movie_review':movie_review,'rate_flag':rate_flag,'update':update,
               'genre':movie.get_my_genre(), 'director':movie.get_my_director(), 'actors': movie.get_my_actor(),
               'language': movie.get_my_language(), 'ott': movie.get_my_ott(), 'country': movie.get_my_country(),
               'all_reviews': movie.reviews(), 'in_watchlist': in_watchlist}
    if upvoted:
        context['upvoted'] = upvoted
    else:
        context['downvoted'] = downvoted
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
        return render(request, 'search.html', {'shows': subset(shows)})

    shows = Show.nodes[0:num_display]
    return render(request, 'mtv.html', {'shows': subset(shows)})

def movies(request):


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)[0:num_display]

        # if request.GET.get('search_query'):
        #     shows = Show.nodes.filter(title__icontains=query)[0:num_display]
        #     header = 'Search Result'
        # else:
        #     shows = Show.get_genre(query, 0, num_display)
        #     header = query + ' Movies'
        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': subset(shows)})


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
        return render(request, 'search.html', {'shows': subset(shows)})

    # shows = Show.nodes[0:num_display]
    movies = Show.get_recadd(0,num_display)
    for show in movies:
        if show.poster_url is None:
            show.poster_url = get_img_url(show.title)
            show.save()

    return render(request, 'recently_added.html', {'shows': subset(movies)})

# MyList functionality
def mylist(request):

    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404


    query = request.GET.get('q')

    if query:
        shows = Show.nodes.filter(title__icontains=query)

        for show in shows:
            if show.poster_url is None:
                show.poster_url = get_img_url(show.title)
                show.save()
        return render(request, 'search.html', {'shows': subset(shows)})

    shows = UserProfile.get_mylist(request.user.username,0,num_display)
    for show in shows:
        print("url:", show.poster_url)
        if show.poster_url is None:
            show.poster_url = get_img_url(show.title)
            show.save()
    # movies = Show.nodes.filter(mylist__watch=True,mylist__user=request.user)
    return render(request, 'mylist.html', {'shows': subset(shows)})


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
        print(username, password)
        user = authenticate(username=username, password=password)

        if user is not None:
            print('user not None')
            if user.is_active:
                print('user active')
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
    user = UserProfile.nodes.get(username=request.user.username)
    context = {'username':user.username,'email':user.email}
    return render(request, 'profile.html', context)

# Edit Profile
# def edit_profile(request):
#     args = {}

#     if request.method == 'POST':
#         form = UpdateProfile(request.POST,instance=request.user)
#         form.actual_user = request.user
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('edit_profile_success'))
#     else:
#         form = UpdateProfile()

#     args['form'] = form
#     return render(request, 'edit_profile.html', args)


# Change Password
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_psw.html', {
        'form': form
    })
