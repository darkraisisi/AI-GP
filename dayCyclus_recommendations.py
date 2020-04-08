import psycopg2
import datetime
from collections import Counter


def get(date1, date2):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='root'")
        cursor = connection.cursor()

        postgreSQL_select_Query = "SELECT products_id FROM cart, sessions WHERE sessions_profiles_id = browser_id AND endtime BETWEEN "+"'"+date1+"'"+" AND "+"'"+date2+"'"


        cursor.execute(postgreSQL_select_Query)
        #print("Selecting rows table using cursor.fetchall")
        records = cursor.fetchall()
        return records

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
                    
def most_bought():
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='root'")
        cursor = connection.cursor()
        periods = [("0-1", ("00","01")), ("1-2", ("01","02")), ("2-3", ("02","03")), ("3-4", ("03","04")), ("4-5", ("04","05")), ("5-6", ("05","06")),
                   ("6-7", ("06","07")), ("7-8", ("07","08")), ("8-9", ("08","09")), ("9-10", ("09","10")), ("10-11", ("10","11")), ("11-12", ("11","12")),
                   ("12-13", ("12","13")), ("13-14", ("13","14")), ("14-15", ("14","15")), ("15-16", ("15","16")), ("16-17", ("16","17")), ("17-18", ("17","18")),
                   ("18-19", ("18","19")), ("19-20", ("19","20")), ("20-21", ("20","21")), ("21-22", ("21","22")), ("22-23", ("22","23")), ("23-24", ("23","00"))]
        for period in periods:
            postgreSQL_select_Query = "SELECT * FROM time_period WHERE time = '"+period[0]+"'"
            cursor.execute(postgreSQL_select_Query)
            purchases = cursor.fetchall()            
            recommendation = 'Nothing'
            recommendation_count = 0
            for purchase in purchases:
                print(purchases.count(purchase), purchase[0], purchase[1])
                if purchases.count(purchase) > recommendation_count:
                    recommendation_count = purchases.count(purchase)
                    recommendation = purchase
            print(recommendation, recommendation_count)
            insert_into_most_bought_time(recommendation)

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)
                    
def insert_into_most_bought_time(values):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='root'")
        cursor = connection.cursor()
        #print(values)
        cursor.execute("""INSERT INTO most_bought_time VALUES({},'{}')""".format(values[0], values[1]))

        connection.commit()
        count = cursor.rowcount
        #print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)

def insert_into_postgres(values):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='root'")
        cursor = connection.cursor()
        #print(values)
        cursor.execute("""INSERT INTO time_period VALUES({},'{}')""".format(values[0], values[1]))

        connection.commit()
        count = cursor.rowcount
        #print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)


def day_periods():
    periods = [("0-1", ("00","01")), ("1-2", ("01","02")), ("2-3", ("02","03")), ("3-4", ("03","04")), ("4-5", ("04","05")), ("5-6", ("05","06")),
               ("6-7", ("06","07")), ("7-8", ("07","08")), ("8-9", ("08","09")), ("9-10", ("09","10")), ("10-11", ("10","11")), ("11-12", ("11","12")),
               ("12-13", ("12","13")), ("13-14", ("13","14")), ("14-15", ("14","15")), ("15-16", ("15","16")), ("16-17", ("16","17")), ("17-18", ("17","18")),
               ("18-19", ("18","19")), ("19-20", ("19","20")), ("20-21", ("20","21")), ("21-22", ("21","22")), ("22-23", ("22","23")), ("23-24", ("23","00"))]
    years = ['2018', '2019']
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    
    for year in years:
        for month in months:
            for int_day in range(1,32):
                if int_day < 10:
                    day = '0'+str(int_day)
                else:
                    day = str(int_day)
                for period in periods:
                    data1 = year+'-'+month+'-'+str(day)+' '+period[1][0]+':00:00'
                    if period[0] == "23-24":
                        data2 = year+'-'+month+'-'+str(day)+' '+period[1][0]+':59:59'
                    else:
                        data2 = year+'-'+month+'-'+str(day)+' '+period[1][1]+':00:00'
                    product = get(data1,data2)
                    product = [item for item, in product]
                    mostcommon = Counter(product).most_common(4)
                    for i in mostcommon:
                        insert_into_postgres((i[0],period[0]))
day_periods()
most_bought()
