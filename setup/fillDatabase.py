import psycopg2

def fill():
    c = psycopg2.connect("dbname=OpisOp user=postgres password=root")
    cur = c.cursor()
    path = 'setup/csv/'
    filenames = ['brand', 'products', 'profiles', 'sessions','cart']

    for filename in filenames:
        with open(path+filename+'.csv', encoding='utf-8') as csvfile:
            print("Copying {}...".format(filename))
            cur.copy_expert("COPY "+filename+" FROM STDIN DELIMITER ',' CSV HEADER", csvfile)
            c.commit()

    c.commit()
    cur.close()
    c.close()