from django_neomodel import DjangoNode
from neomodel import db
from neomodel import (
    StringProperty,
    IntegerProperty,
    FloatProperty,
    BooleanProperty,
    StructuredNode,
    EmailProperty,
    RelationshipTo,
    RelationshipFrom,
    Relationship,
    UniqueIdProperty,
    DateProperty,
    RelationshipFrom,
    RelationshipTo,
    One,
)


class Person(StructuredNode):
    person_id = UniqueIdProperty()
    name = StringProperty(max_length=250)
    dob = DateProperty()
    gender = StringProperty(max_length=10)

    def __str__(self):
        return self.name


class Ott(StructuredNode):
    name = StringProperty(max_length=250)

    def __str__(self):
        return self.name

class Genre(StructuredNode):
    name = StringProperty(max_length=250)

    def __str__(self):
        return self.name

class Language(StructuredNode):
    name = StringProperty(max_length=250)

    def __str__(self):
        return self.name

class Country(StructuredNode):
    name = StringProperty(max_length=250)

    def __str__(self):
        return self.name

class Show(StructuredNode):
    # show_id                          = UniqueIdProperty()
    title                       = StringProperty(unique_index=True, required=True,max_length=250)
    show_logo                   = StringProperty()
    duration                    = IntegerProperty()
    # release_date                = DateProperty(default='2000-01-01')
    release_year                = IntegerProperty()
    avg_rating                  = FloatProperty()
    imdb_rating                 = FloatProperty()
    #imdb_id = CharField(max_length=250)
    rotten_tomato               = IntegerProperty()
    budget                      = IntegerProperty()
    overview                    = StringProperty(max_length=1000)
    overall_rating              = FloatProperty()
    is_movie                    = BooleanProperty(default=False)
    origin_country              = RelationshipTo(Country, 'ORIGIN_COUNTRY')
    origin_language             = RelationshipTo(Language, 'ORIGIN_LANGUAGE')
    genre                       = RelationshipTo(Genre, 'genre')
    available_on                = RelationshipTo(Ott, 'AVAILABLE_ON')
    actors                      = RelationshipTo(Person, "ACTORS")
    director                    = RelationshipTo(Person, "DIRECTOR")

    def genre(g):
        show_list, meta = db.cypher_query(f'MATCH (a)-[:genre]->(b{{name:"{g}"}}) RETURN a')
        return [Show.inflate(row[0]) for row in show_list]

    def top_movies():
        top_list, meta = db.cypher_query('MATCH (a:Show)  RETURN a ORDER BY COALESCE(a.imdb_rating,0) DESC')
        print(top_list[0:10])
        # for t in top_list[0:10]:
        #     print(t[0].imdb_rating)
        return [Show.inflate(row[0]) for row in top_list]


    def __str__(self):
        return self.title


class Rating(StructuredNode):
    id = UniqueIdProperty()
    numeric = FloatProperty()
    review = StringProperty(max_length=1000)
    upvotes = IntegerProperty()
    downvotes = IntegerProperty()



class UserProfile(DjangoNode):
    # person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
    person_id = RelationshipTo(Person, "PERSON", cardinality=One)
    username = StringProperty(max_length=250, unique_index=True, required=True)
    email = EmailProperty()
    # password = StringProperty(max_length=250)
    nationality = RelationshipTo(Country, "NATIONALITY", cardinality=One)
    language_preference = RelationshipTo(Language, "LANGUAGE_PREFERENCE")
    watchlist = RelationshipTo(Show, "WATCHLIST")



# class OriginCountry(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
#     country_id = models.ForeignKey(Country, on_delete=models.CASCADE)



# class OriginalLanguage(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete=models.CASCADE)
#     language_id = models.ForeignKey(Language, on_delete=models.CASCADE)

# class Genre_of(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     genre_id = models.ForeignKey(Genre, on_delete = models.CASCADE)

# class Available(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     ott_id = models.ForeignKey(Ott, on_delete = models.CASCADE)



# class LangPreference(StructuredNode):
#     person_id = RelationshipTo(Person, cardinality=)
#     language_id = models.ForeignKey(Language, on_delete = models.CASCADE)

# class WatchList(StructuredNode):
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)


# class Mru(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     username = models.ForeignKey(User, on_delete = models.CASCADE)
#     rating_id = models.ForeignKey(Rating, on_delete = models.CASCADE)


# class Actor(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     #role = StringProperty(max_length=100)

# class Director(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     #role = StringProperty(max_length=100)

# class Show(StructuredNode):
#     id = UniqueIdProperty(primary_key=True)
#     title = StringProperty(max_length=250)
#     overview = StringProperty(max_length=1000)
#     overall_rating = models.DecimalField(decimal_places=2, max_digits=4)
#     is_movie = models.BooleanField(default=False)
#     origin_country = models.ForeignKey(Country, on_delete=models.CASCADE, default=1)
#
#     def __str__(self):
#         return self.title + " - " + self.overview + ", " + self.origin_country + ", " + self.original_language



# class Episode(StructuredNode):
#     id = UniqueIdProperty(primary_key=True)
#     episode_of = models.ForeignKey(Show, on_delete=models.CASCADE)
#     title = StringProperty(max_length=250)
#     duration = models.DurationField()
#     release_date = DateProperty()
#     avg_rating = models.DecimalField(decimal_places=2, max_digits=4)
#     imdb_rating = models.DecimalField(decimal_places=2, max_digits=4)
#     imdb_id = StringProperty(max_length=250)
#     rotten_tomato = models.IntegerField()
#     budget = models.BigIntegerField()
#     overview = StringProperty(max_length=1000)
#
#     def __str__(self):
#         return self.title

# class CastMember(StructuredNode):
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     profession = StringProperty(max_length=250)
#
# class CrewMember(StructuredNode):
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     profession = StringProperty(max_length=250)

# class Cast(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     role = StringProperty(max_length=100)
#
# class Crew(StructuredNode):
#     show_id = models.ForeignKey(Show, on_delete = models.CASCADE)
#     # episode_id = models.ForeignKey(Episode, on_delete = models.CASCADE)
#     person_id = models.ForeignKey(Person, on_delete = models.CASCADE)
#     role = StringProperty(max_length=100)
