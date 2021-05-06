from django.urls import path
from . import views
# app_name = 'Movie'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signUp, name='signup'),
    path('login/', views.Login, name='login'),
    path('profile/', views.account, name='account'),
    path('logout/', views.Logout, name='logout'),
    path('search/',views.search, name='search'),
    path('<int:movie_id>/', views.detail, name='detail'),
    path('mylist/', views.mylist, name='mylist'),
    path('recently_added', views.recently_added, name='recently_added'),
    path('movies', views.movies, name='movies'),
    path('tv_shows', views.tv_shows, name='tv_shows'),
]
