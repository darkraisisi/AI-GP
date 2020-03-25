import psycopg2


""" Run this file to generate the whole database, you only need to personify the parameters of the postgresql database to acces your database """
path = 'database/'
def run():

    connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database="OpisOp")
    cursor = connection.cursor()
    with cursor as cursor:
        cursor.execute(open(path+"db_postgres.sql", "r", encoding='utf-8').read())

    connection.commit()
    cursor.close()
    connection.close()
    print("PostgreSQL datebase is generated")