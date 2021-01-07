import sqlite3, web
from sqlite3 import Error


def create_table(name):

    name = str(name).replace(' ', '_').replace('-', '_').replace('+', '_').lower()

    conn = None

    try:
        conn = sqlite3.connect("db.sqlite")
        conn.execute(f'''CREATE TABLE IF NOT EXISTS {name}
                        (
                            ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                            single_core_score INTEGER NOT NULL,
                            multi_core_score INTEGER NOT NULL
                        )
                    ''')

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()


def is_table_exist(name):

    name = str(name).replace(' ', '_').replace('-', '_').replace('+', '_').lower()

    conn = sqlite3.connect('db.sqlite')
    c = conn.cursor()
                
    #get the count of tables with the name
    c.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}' ''')
    
    exist = False
    #if the count is 1, then table exists
    if c.fetchone()[0] == 1 :
        exist = True
                		
    conn.commit()
    conn.close()

    return exist


def get_table_column(table, column):

    # Define sqlite table
    table = str(table).replace(' ', '_').replace('-', '_').replace('+', '_').lower()

    result = []
    conn = None

    try:
        conn = sqlite3.connect("db.sqlite")
        cur = conn.cursor()
        cur.execute(f"SELECT {column} FROM {table}")

        rows = cur.fetchall()

        for row in rows:
            result += [int(row[0])]

    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

        return result


def insert_rows(table, values_2d):

    table = str(table).replace(' ', '_').replace('-', '_').replace('+', '_').lower()

    try:
        conn = sqlite3.connect("db.sqlite")
        
        for values in values_2d:
            conn.execute(f'''INSERT INTO {table} (single_core_score, multi_core_score) VALUES ({', '.join(str(x) for x in values)})''')

        conn.commit()
        
    except Error as e:
        print(e)

    finally:
        if conn:
            conn.close()

