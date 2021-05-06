from collections import defaultdict
from django.apps import apps
import csv
from movie.models import Ott,Genre,Language,Country,Show,Person

class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))


filename = "../../kaggle_datasets/movies.csv"

platform = {0:'Netflix',
            1:'Hulu',
            2:'Prime',
            3:'Disney'}

(Ott(name='Netflix')).save()
(Ott(name='Hulu')).save()
(Ott(name='Prime')).save()
(Ott(name='Disney')).save()


with open(filename, 'r',encoding='utf-8') as csv_file:

    csvreader = csv.reader(csv_file)
    fields = next(csvreader)
    ind = 0
    for row in csvreader:

        # show
        leng = len(row)
        for i in range(leng):
            if row[i]=="":
                row[i]=None
        if row[5] is not None:
            row[5] = int(row[5].split("%")[0])

        s = (Show(title=row[1], duration=row[15], release_year=row[2], imdb_rating=row[4], rotten_tomato = row[5])).save()
        ind = ind+1
        # if ind==10:
        #     break
        if ind%1000==0:
            print(ind)

        # available
        for i in range(4):
            if (row[i+6]=='1'):
                s.available_on.connect(Ott.nodes.get(name=platform[i]))
        #
        # genre
        list_g = row[12]
        if list_g is not None:
            for genre in list_g.split(","):
                g = Genre.nodes.get_or_none(name=genre)
                if g is None:
                    g = (Genre(name = genre)).save()
                s.genre.connect(g)

        # language
        list_l = row[14]
        if list_l is not None:
            for lang in list_l.split(","):
                l = Country.nodes.get_or_none(name=lang)
                if l is None:
                    l = (Language(name = lang)).save()
                s.origin_language.connect(l)

        # country
        list_c = row[13]
        if list_c is not None:
            for country in list_c.split(","):
                c = Country.nodes.get_or_none(name=country)
                if c is None:
                    c = (Country(name = country)).save()
                s.origin_country.connect(c)

        # director
        list_d = row[11]
        if list_d is not None:
            for dir in list(set(list_d.split(","))):
                p = Person.nodes.get_or_none(name=dir)
                if p is None:
                    num = len(Person.nodes) + 1
                    p = (Person(person_id = num,name=dir)).save()
                s.director.connect(p)
