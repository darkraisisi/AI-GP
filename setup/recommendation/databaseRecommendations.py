import psycopg2

def run():

    connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database="OpisOp")
    cursor = connection.cursor()
    with cursor as cursor:
        cursor.execute(open("setup/recommendation/recommendation.sql", "r", encoding='utf-8').read())

    connection.commit()
    cursor.close()
    connection.close()
    print("PostgreSQL datebase is alterd with recommendations tables")