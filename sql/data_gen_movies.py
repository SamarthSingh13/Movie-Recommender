import psycopg2, config, exec
import csv

filename = "../kaggle_datasets/movies.csv"
fields = []
rows = []


# id int, 0
# Title text, 1
# Year int, 2
# Age text, 3
# IMDb float, 4
# Rotten_Tomatoes text, 5
# Netflix int, 6
# Hulu int, 7
# Prime int, 8
# Disney int, 9
# Type int, 10
# Directors text[], 11
# Genres text[], 12
# Country text[], 13
# Language text[], 14
# Runtime int, 15
g = 1
g_list = []
l = 1
l_list = []
d = 1
d_list = []
c = 1
c_list = []
j = 0

conn = exec.connect()
crsr = conn.cursor()

query = "SELECT count(*) FROM show;"
crsr.execute(query)
num = crsr.fetchall()[0][0] + 1

query = "INSERT INTO ott VALUES (1,'Netflix'), (2,'Hulu'), (3,'Prime'), (4,'Disney');"
crsr.execute(query)

with open(filename, 'r',encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    # extracting each data row one by one
    for row in csvreader:
        row[0] = num
        num += 1
        # show
        leng = len(row)
        for i in range(leng):
            if row[i]=="":
                row[i]=None
        query_insert = "INSERT INTO show(id,title,duration,release_year,imdb_rating,rotten_tomato,is_movie) VALUES (%s, %s, %s, %s, %s, %s, 1-%s);"
        crsr.execute(query_insert,(row[0],row[1],row[15],row[2],row[4],row[5],row[10]))

        # available
        for i in range(4):
            if (row[i+6]=='1'):
                query_insert = "INSERT INTO available VALUES (%s,%s);"
                crsr.execute(query_insert,(row[0],i+1,))

        # genre
        list_g = row[12]
        if list_g is not None:
            for genre in list_g.split(","):
                if genre not in g_list:
                    g_list.append(genre)
                    query_insert = "INSERT INTO genre VALUES (%s,%s);"
                    crsr.execute(query_insert,(g,genre,))
                    g+=1
                query_insert = "INSERT INTO genre_of VALUES (%s,%s);"
                crsr.execute(query_insert,(row[0],g_list.index(genre)+1,))

        # language
        list_l = row[14]
        if list_l is not None:
            for lang in list_l.split(","):
                if lang not in l_list:
                    l_list.append(lang)
                    query_insert = "INSERT INTO language VALUES (%s,%s);"
                    crsr.execute(query_insert,(l,lang,))
                    l+=1
                query_insert = "INSERT INTO original_language VALUES (%s,%s);"
                crsr.execute(query_insert,(row[0],l_list.index(lang)+1,))

        # director
        list_d = row[11]
        if list_d is not None:
            for dir in list(set(list_d.split(","))):

                if dir not in d_list:
                    d_list.append(dir)
                    query_insert = "INSERT INTO person VALUES (%s,%s,NULL,NULL);"
                    crsr.execute(query_insert,(d,dir,))
                    d+=1
                query_insert = "INSERT INTO director VALUES (%s,%s);"
                crsr.execute(query_insert,(row[0],d_list.index(dir)+1,))

        # country
        list_c = row[13]
        if list_c is not None:
            for country in list_c.split(","):
                if country not in c_list:
                    c_list.append(country)
                    query_insert = "INSERT INTO country VALUES (%s,%s);"
                    crsr.execute(query_insert,(c,country,))
                    c+=1
                query_insert = "INSERT INTO origin_country VALUES (%s,%s);"
                crsr.execute(query_insert,(row[0],c_list.index(country)+1,))
conn.commit()
conn.close()
# except Exception as err:
#     print("ERROR %%%%%%%%%%%%%%%% \n", err)
