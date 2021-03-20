import psycopg2, config

def connect():
    """ returns connection to database """
    # TODO: use variables from config file as connection params
    conn = psycopg2.connect(database = config.name,user = config.user,password = config.pswd,host = config.host,port = config.port)
    return conn

    pass

def exec_query(conn, sql):
    """ Executes sql query and returns header and rows """
    # TODO: create cursor, get header from cursor.description, and execute query to fetch rows.
    crsr = conn.cursor()
    crsr.execute(sql)
    header = [i[0] for i in crsr.description]
    rows = crsr.fetchall()
    return (header, rows)

    pass

if __name__ == "__main__":
    from sys import argv
    import config

    query = argv[1]
    try:
        conn = connect()
        (header, rows) = exec_query(conn, query)
        print(",".join([str(i) for i in header]))
        for r in rows:
            print(",".join([str(i) for i in r]))
        conn.close()
    except Exception as err:
        print("ERROR %%%%%%%%%%%%%%%% \n", err)
