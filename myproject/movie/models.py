from django_neomodel import DjangoNode
import numpy as np
from scipy.sparse import csr_matrix
from neomodel import db
import random

from neomodel import (
    StringProperty,
    IntegerProperty,
    FloatProperty,
    BooleanProperty,
    StructuredNode,
    StructuredRel,
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
    # show_id                     = UniqueIdProperty()
    title                       = StringProperty(unique_index=True, required=True,max_length=250)
    poster_url                  = StringProperty()
    duration                    = IntegerProperty()
    # release_date                = DateProperty(default='2000-01-01')
    release_year                = IntegerProperty()
    imdb_rating                 = FloatProperty()
    #imdb_id = CharField(max_length=250)
    rotten_tomato               = IntegerProperty()
    budget                      = IntegerProperty()
    overview                    = StringProperty(max_length=1000)
    overall_rating              = FloatProperty()
    num_votes                   = IntegerProperty(default=0)
    is_movie                    = BooleanProperty(default=False)
    origin_country              = RelationshipTo(Country, 'ORIGIN_COUNTRY')
    origin_language             = RelationshipTo(Language, 'ORIGIN_LANGUAGE')
    genre                       = RelationshipTo(Genre, 'genre')
    available_on                = RelationshipTo(Ott, 'AVAILABLE_ON')
    actors                      = RelationshipTo(Person, "ACTORS")
    director                    = RelationshipTo(Person, "DIRECTOR")

    def get_by_id(show_id):
        query = f"MATCH (a) WHERE ID(a)={show_id} RETURN a"
        results, meta = db.cypher_query(query)
        return Show.inflate(results[0][0]) if results[0] else None

    def reviews(self):
        results, columns = self.cypher(f"MATCH (u:UserProfile)-[r:RATINGS]->(b) WHERE id(b)={self.id} AND EXISTS(r.review) RETURN u, r")
        return [(UserProfile.inflate(row[0]).username, Rating.inflate(row[1])) for row in results]

    def get_my_genre(self):
        s = ""
        for g in self.genre:
            s += g.name + " | "
        return s[:-2]

    def get_my_director(self):
        s = ""
        for d in self.director:
            s += d.name + ", "
        return s[:-2]

    def get_my_actor(self):
        s = ""
        for d in self.actors:
            s += d.name + ", "
        return s[:-2]

    def get_my_country(self):
        s = ""
        for c in self.origin_country:
            s += c.name + " | "
        return s[:-2]

    def get_my_language(self):
        s = ""
        for l in self.origin_language:
            s += l.name + " | "
        return s[:-2]

    def get_my_ott(self):
        s = ""
        for o in self.available_on:
            s += o.name + " | "
        return s[:-2]

    def get_genre(g, offset, limit):
        show_list, meta = db.cypher_query(f'MATCH (a)-[:genre]->(b{{name:"{g}"}}) RETURN a SKIP {offset} LIMIT {limit}')
        return [Show.inflate(row[0]) for row in show_list]

    def top_movies(offset, limit):
        top_list, meta = db.cypher_query(f'MATCH (a:Show)  RETURN a ORDER BY COALESCE(a.imdb_rating,0) DESC SKIP {offset} LIMIT {limit}')
        # print(top_list[0:10])
        # for t in top_list[0:10]:
        #     print(t[0].imdb_rating)
        return [Show.inflate(row[0]) for row in top_list]

    def get_recadd(offset,limit):
        recent_list, meta = db.cypher_query(f'MATCH (a:Show)  RETURN a ORDER BY a.release_year DESC SKIP {offset} LIMIT {limit}')
        return [Show.inflate(row[0]) for row in recent_list]

    def __str__(self):
        return self.title


class Rating(StructuredRel):
    # id = UniqueIdProperty()
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
    ratings = RelationshipTo(Show, "RATINGS", model=Rating)

    # def get_usermovie_ratings(self):
    #     db.cypher_query("MATCH (u:UserProfile)-[r:Rating]->(s:Show) WHERE id(u) <> {self} RETURN ")

    def get_mylist(uname,offset,limit):
        show_list, meta = db.cypher_query(f'MATCH (a{{username:"{uname}"}})-[:WATCHLIST]->(b) RETURN b SKIP {offset} LIMIT {limit}')
        return [Show.inflate(row[0]) for row in show_list]


    def recommendations(self, k, n):
        # mymovie_ratings, mycolumns = self.cypher("MATCH (u:UserProfile)-[r:Rating]->(s:Show) WHERE id(u) = {self} RETURN u,r,s")
        shows = Show.nodes.all()
        print("length shows", len(shows))
        showDict = {show.id:i for i, show in enumerate(shows)}
        mywatch_set = set()

        users = UserProfile.nodes.all()
        # print("Users")
        # for u in users:
        #     print(u)
        userDict = {user.id:i for i, user in enumerate(users)}

        movie_ratings, _ = self.cypher("MATCH (u:UserProfile)-[r:RATINGS]->(s:Show) RETURN u,r,s")
        movie_ratings = [(UserProfile.inflate(row[0]), Rating.inflate(row[1]), Show.inflate(row[2])) for row in movie_ratings]

        # print("movie_ratings")
        # for mr in movie_ratings:
        #     print(mr)

        mymovie_ratings = np.zeros((len(Show.nodes),))

        def f(r, s):
            mymovie_ratings[showDict[s.id]] = r.numeric
            mywatch_set.add(showDict[s.id])
            return False
        movie_ratings = [(u.id, r.numeric, s.id) for (u, r, s) in movie_ratings if (u.id != self.id or f(r, s))]

        # mymovie_ratings = [self.inflate(row[0]) for row in mymovie_ratings]



        #usermovie_ratings exists, othersmovie_ratings

        # n = 20 # num_users
        # k = 10 # num_movies
        # print("mymovie_ratings")
        # for mmr in mymovie_ratings:
        #     print(mmr)

        print("my_num_rated", np.sum(mymovie_ratings != 0.0))

        row_list = list(map(lambda x: userDict[x[0]], movie_ratings))
        val_list = list(map(lambda x: x[1], movie_ratings))
        col_list = list(map(lambda x: showDict[x[2]], movie_ratings))

        usermovie_ratings = csr_matrix((val_list, (row_list, col_list)), shape=(len(UserProfile.nodes), len(Show.nodes)))
        usermovie_ratings = usermovie_ratings.todense()
        print("usermovie_ratings", usermovie_ratings)

        # cosine_similarities = [np.dot(mymovie_ratings, usermovie_ratings) / (np.linalg.norm(mymovie_ratings) * np.linalg.norm(usermovie_ratings)) for usermovie_ratings in othersmovie_ratings]
        cosine_similarities = [(i, np.dot(usermovie_ratings[i,:], mymovie_ratings) / (1e-10 + (np.linalg.norm(mymovie_ratings) * np.linalg.norm(usermovie_ratings[i,:])))) for i in range(len(usermovie_ratings))]

        cosine_similarities.sort(key = lambda x: x[1], reverse=True)
        topn_users = cosine_similarities if len(UserProfile.nodes)<n else cosine_similarities[:n]

        # np.array(usermovie_ratings)[list(map(lambda x: x[0], topn_users)) :]
        topn_users_indices = list(map(lambda x: x[0], topn_users))
        topn_users_scores = list(map(lambda x: x[1].item((0,0)), topn_users))
        print("topn_users", topn_users_indices)
        print("topn_scores", topn_users_scores)

        topn_users_ratings = np.squeeze(np.array([usermovie_ratings[i,:] for i in topn_users_indices]))
        print("topn_users_ratings")
        print(topn_users_ratings)

        if all(np.array(topn_users_scores) == 0.0):
            x = list(range(0, len(Show.nodes)))
            random.shuffle(x)
            print("list of movies", list(map(lambda x: shows[x], x[:k])))
            return list(map(lambda x: shows[x], x[:k]))
            # return list(map(lambda x: shows[x], list(range(0,k))))

        predicted_ratings = np.average(topn_users_ratings, axis=0, weights=topn_users_scores)
        print("len_predicted_ratings", len(predicted_ratings))

        predicted_ratings = list(enumerate(predicted_ratings))
        predicted_ratings = list(filter(lambda x: x[0] not in mywatch_set, predicted_ratings))

        predicted_ratings.sort(key = lambda x: x[1], reverse=True)
        print("predicted_ratings", predicted_ratings)

        topk_movies = predicted_ratings if len(Show.nodes)<k else predicted_ratings[:k]
        print("topk_movies")
        for topkmovie in topk_movies:
            print(topkmovie)

        return list(map(lambda x: shows[x[0]], topk_movies))

# https://api.themoviedb.org/3/search/movie?api_key=5ee2bfd3c10aaeb6eefd31d8242fb986&query=jaws



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
