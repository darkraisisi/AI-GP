import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DBMS
con = psycopg2.connect("dbname = OpisOp user=postgres password='wachtwoord'")
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