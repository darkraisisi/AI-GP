import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS
con = psycopg2.connect("dbname = OpisOp user=postgres password='root'")
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()


def create_tables():
    commands = (
        '''
        CREATE TABLE most_bought_day
        (
        product_id varchar,
        day timestamp,
        FOREIGN KEY (product_id) references products(id)
        )
        ''',
        '''
        CREATE TABLE cart_recommendations
        (
        product_cart_id varchar,
        product_recommendation_id varchar,
        FOREIGN KEY (product_cart_id) references products(id),
        FOREIGN KEY (product_recommendation_id) references products(id)
        )
        ''',
        '''
        CREATE TABLE most_bought_period
        (
        product_id varchar,
        timeperiod varchar,
        FOREIGN KEY (product_id) references products(id)
        )
        ''',
        '''
        CREATE TABLE time_period
        (
        product_id varchar,
        time varchar,
        FOREIGN KEY (product_id) references products(id)
        )
        '''
        ,
        '''
        CREATE TABLE most_bought_time
        (
        product_id varchar,
        time varchar,
        FOREIGN KEY (product_id) references products(id)
        )
        '''
    )


    try:
        for command in commands:
            cursor.execute(command)

        cursor.close()
        con.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if con is not None:
            con.close()


create_tables()
