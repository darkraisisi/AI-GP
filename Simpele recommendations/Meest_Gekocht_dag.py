'''
Bron 1: https://stackoverflow.com/questions/6987285/python-find-the-item-with-maximum-occurrences-in-a-list
'''

import psycopg2


def get(date1, date2):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='wachtwoord'")
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT products_id FROM cart, sessions WHERE sessions_profiles_id = browser_id AND starttime BETWEEN "+"'"+date1+"'"+" AND "+"'"+date2+"'"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from products table using cursor.fetchall")
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def insert_into_postgres(table, values):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='wachtwoord'")
        cursor = connection.cursor()


        if table == "most_bought_day":
            cursor.execute("""INSERT INTO most_bought_day VALUES({},{})""".format(values[0], values[1]))


        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

def recommendation():
    #   Je geeft 2 data op van de dagen waartussen je de records wil krijgen
    #   Wil je de records van 1 dag, bijvoorbeeld 2017-12-10 dan doe je get('2017-12-10', '2017-12-11').

    data = get('2017-12-18', '2017-12-19')
    dag = ("2017-12-18")
    data = [item for item, in data]

    for x in range(0,3):
        item = max(data,key=data.count)
        insert_into_postgres("most_bought_day", (item, "'"+dag+"'"))
        for a in data:
            if a == item:
                data.remove(a)




recommendation()