import psycopg2

def get(colom, table, limit):
    try:
        connection = psycopg2.connect("dbname = OpisOp user=postgres password='wachtwoord'")

        cursor = connection.cursor()

        if limit == '':
            postgreSQL_select_Query = "select " +colom+" from " + table
        else:
            postgreSQL_select_Query = "select "+colom+" from "+table+" limit "+limit

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

        if table == "cart_recommendations":
            cursor.execute("""INSERT INTO cart_recommendations VALUES({},{})""".format(values[0], values[1]))

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Failed to insert record into table", error)


def cart_recommendation():
    records = get("*", "products",'10000')

    recommended_ids = []
    already_added = []

    for product_cart in records:
        for product_recommend in records:
            # Categorie moet hetzelfde zijn, maar subcategorie anders
            if product_cart != product_recommend and product_cart[4] == product_recommend[4] and \
                    product_cart[5] != product_recommend[5] \
                    and ([product_cart[0],product_recommend[0]]) not in already_added \
                    and ([product_recommend[0],product_cart[0]]) not in already_added:
                already_added.append([product_cart[0], product_recommend[0]])
                insert_into_postgres("cart_recommendations", (product_cart[0],product_recommend[0]))
                break

cart_recommendation()