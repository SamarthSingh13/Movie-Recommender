from django.db import models

# Create your models here.
class Ott(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# class Show(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=250)
#     overview = models.CharField(max_length=1000)
#     overall_rating = models.DecimalField(decimal_places=2, max_digits=4)
#     is_movie = models.BooleanField(default=False)
#     origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
#
#     def __str__(self):
#         return self.title + " - " + self.overview + ", " + self.origin_country + ", " + self.original_language

class OriginalLanguage(models.Model):
    show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
    language_id = models.ForeignKey(Language, on_delete=models.CASCADE)

class Show(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    duration = models.DurationField()
    release_date = models.DateField()
    avg_rating = models.DecimalField(decimal_places=2, max_digits=4)
    imdb_rating = models.DecimalField(decimal_places=2, max_digits=4)
    imdb_id = models.CharField(max_length=250)
    rotten_tomato = models.IntegerField()
    budget = models.BigIntegerField()
    overview = models.CharField(max_length=1000)
    overall_rating = models.DecimalField(decimal_places=2, max_digits=4)
    is_movie = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " - " + self.overview

# class Episode(models.Model):
#     id = models.AutoField(primary_key=True)
#     episode_of = models.ForeignKey(Show, on_delete=models.CASCADE)
#     title = models.CharField(max_length=250)
#     duration = models.DurationField()
#     release_date = models.DateField()
#     avg_rating = models.DecimalField(decimal_places=2, max_digits=4)
#     imdb_rating = models.DecimalField(decimal_places=2, max_digits=4)
#     imdb_id = models.CharField(max_length=250)
#     rotten_tomato = models.IntegerField()
#     budget = models.BigIntegerField()
#     overview = models.CharField(max_length=1000)
#
#     def __str__(self):
#         return self.title

class Genre_of(models.Model):
    show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
    # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete = models.CASCADE)

class Available(models.Model):
    show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
    # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
    ott_id = models.ForeignKey(Ott, on_delete = models.CASCADE)


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    nationality = models.ForeignKey(Country, on_delete = models.CASCADE, default=1)

    def __str__(self):
        return self.name

class LangPreference(models.Model):
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    language_id = models.ForeignKey(Language, on_delete = models.CASCADE)

class WatchList(models.Model):
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
    # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)

class CastMember(models.Model):
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    profession = models.CharField(max_length=250)

class CrewMember(models.Model):
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    profession = models.CharField(max_length=250)

class User(models.Model):
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    user_id = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=250)

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    numeric = models.DecimalField(decimal_places=2, max_digits=4)
    review = models.CharField(max_length=1000)
    upvotes = models.IntegerField()
    downvotes = models.IntegerField()

class Mru(models.Model):
    show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
    # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    rating_id = models.ForeignKey(Rating, on_delete = models.CASCADE)

class Cast(models.Model):
    show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
    # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    role = models.CharField(max_length=100)

class Crew(models.Model):
    show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
    # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    role = models.CharField(max_length=100)
