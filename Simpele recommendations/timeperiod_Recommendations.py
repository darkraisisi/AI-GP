'''
Bron 1: https://stackoverflow.com/questions/6987285/python-find-the-item-with-maximum-occurrences-in-a-list
'''

import psycopg2
import datetime
from collections import Counter

def get(date1, date2):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='wachtwoord'")
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT products_id FROM cart, sessions WHERE sessions_profiles_id = browser_id AND starttime BETWEEN "+"'"+date1+"'"+" AND "+"'"+date2+"'"


        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows table using cursor.fetchall")
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

        if table == "most_bought_period":
            cursor.execute("""INSERT INTO most_bought_period VALUES({},{},{})""".format(values[0], values[1], values[2]))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

def average_year():
    average_data = get("2018-01-1", "2018-12-31")
    average_data = [item for item, in average_data]
    mostcommon_year = Counter(average_data).most_common(1000)
    return mostcommon_year


def most_bought_daily():
    #   Je geeft 2 data op van de dagen waartussen je de records wil krijgen
    #   Wil je de records van 1 dag, bijvoorbeeld 2017-12-10 dan doe je get('2017-12-10', '2017-12-11').

    data = get('2017-12-18', '2017-12-19')
    dag = ("2017-12-18")
    data = [item for item, in data]

    #   Dit werkt niet, maar als de op=op voordeelshop nog echt zou opereren zou dit gebruikt kunnen worden
    #   In plaats van handmatig de dag in te voeren
    # dag_ = datetime.date.today()
    # dag_2 = datetime.date.today() + datetime.timedelta(days=1)
    # data_ = get(dag_, dag_2)
    # data_ = [item for item, in data_]




    mostcommon = Counter(data).most_common(3)
    for x in mostcommon:
        insert_into_postgres("most_bought_day", (x[0], "'" + dag + "'"))


#   Tijdperiodes
#   Jaargetijden: Lente(1 maart t/m 31 mei), Zomer(1 juni t/m 31 augustus), Herfst(1 september t/m 30 november), Winter(1 december t/m 28 februari)
#   Speciale periodes: Sinterklaas(21 november t/m 5 december), Kerst (10 december t/m 25 december)
def time_periods():
    # Lente = ("Lente", ("2018-03-01","2018-05-31"))
    # Zomer = ("Zomer",("2018-06-01","2018-08-31"))
    # Herfst = ("Herfst", ("2018-09-01", "2018-11-30"))
    # Winter = ("Winter", ("2017-12-01", "2018-02-28"))
    # Sinterklaas = ("Sinterklaas", ("2018-11-21", "2018-12-05"))
    # Kerst = ("Kerst", ("2018-12-10", "2018-12-25"))

    periods = [("Lente", ("2018-03-01","2018-05-31")), ("Zomer",("2018-06-01","2018-08-31")), ("Herfst", ("2018-09-01", "2018-11-30")),
               ("Winter", ("2017-12-01", "2018-02-28")), ("Sinterklaas", ("2018-11-21", "2018-12-05")),("Kerst", ("2018-12-10", "2018-12-25"))]
    seasons = ["Lente", "Zomer", "Herfst", "Winter"]


    average_prodid_amount = average_year()
    average_prodidonly = []


    for item in average_prodid_amount:
        average_prodidonly.append(item[0])

    for period in periods:
        data = get(period[1][0], period[1][1])
        data = [item for item, in data]
        period_name = period[0]

        mostcommon = Counter(data).most_common(1000)

        products_added = 0
        for x in mostcommon:
            if products_added >= 10:
                break

            for item in average_prodid_amount:
                if item[0] == x[0]:
                    current_average = item   # Het gemiddelde van het hele jaar in de vorm [prodid, aantal x gekocht]
                    break

            if x[0] not in average_prodidonly:
                insert_into_postgres("most_bought_period", (x[0], "'" + period_name + "'", x[1]))
                products_added += 1

            elif period_name in seasons:
                if x[1]*4 > current_average[1]*2:
                    insert_into_postgres("most_bought_period", (x[0], "'" + period_name + "'", x[1]))
                    products_added += 1
            elif x[1]*24 > current_average[1]*2:
                insert_into_postgres("most_bought_period", (x[0], "'" + period_name + "'", x[1]))
                products_added += 1



time_periods()