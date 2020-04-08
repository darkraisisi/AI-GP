import psycopg2
import pyowm
from datetime import date
from datetime import datetime, timedelta
from collections import Counter

year = 365
amount_of_years_in_history = 2

today = datetime.strftime(datetime.now() - timedelta((year*amount_of_years_in_history)+0), '%Y-%m-%d')
yesterday = datetime.strftime(datetime.now() - timedelta((year*amount_of_years_in_history)+1), '%Y-%m-%d')
print(today,yesterday)
own = pyowm.OWM('bc3621df57d305370c47b0879f74aee9')
city = input('What city do you wish to observe? ')
observation = own.weather_at_place(city)
weather = observation.get_weather()
temperature = weather.get_temperature('celsius')['temp']

# Om erachter te komen op welke humidity levels het precies gaat regenen, moet je verschillende formules toe passen.
# Voor het gemak zeggen we dat als humidity >= 100%, dan regent het.

humidity = weather.get_humidity()
status = weather.get_detailed_status()

def get(date1, date2):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password=root")
        cursor = connection.cursor()

        postgresSQL_select_Query = 'SELECT c.products_id FROM cart AS c INNER JOIN sessions AS s ON c.sessions_profiles_id = s.browser_id WHERE s.starttime BETWEEN ' + "'" + date1 + "'" + " AND " + "'" + date2 + "'"

        cursor.execute(postgresSQL_select_Query)
        records = cursor.fetchall()

        return records[:10]

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgresSQL", error)


def insert_postgres(table, values):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password=root")
        cursor = connection.cursor()

        if table == "weers_omstandigheden":
            cursor.execute("""INSERT INTO weers_omstandigheden VALUES(%s,%s,%s,%s,%s)""",(values[0], values[1], values[2], values[3], values[4]))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

def most_bought_daily():
    data = get(str(yesterday), str(today))
    data = [item for item, in data]

    most_bought = Counter(data).most_common(3)
    
    most_bought_no_counter = []
    for item in most_bought:
        most_bought_no_counter.append(item[0])

    return most_bought_no_counter


insert_postgres('weers_omstandigheden', [today, city, temperature, humidity, most_bought_daily()])