from collections import defaultdict
from django.apps import apps
import csv
from movie.models import Ott,Genre,Language,Country,Show,Person
from neomodel import db

filename = "../../kaggle_datasets/movies.csv"

with db.transaction:
    p0 = (Ott(name='Netflix')).save()
    p1 = (Ott(name='Hulu')).save()
    p2 = (Ott(name='Prime')).save()
    p3 = (Ott(name='Disney')).save()
    platform = {0:p0,
                1:p1,
                2:p2,
                3:p3}


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
                    s.available_on.connect(platform[i])
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
            s.save()
