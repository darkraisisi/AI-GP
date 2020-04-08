import psycopg2
import csv
from datetime import datetime

connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database="OpisOp")

cursor = connection.cursor()

def run():
    collab_recommendations(
        ['BOUNCER','JUDGER','LEAVER','BUYER','BROWSER','COMPARER','FUN_SHOPPER'],
        ['Unisex','Kinderen','Senior','B2B','Gezin','Baby','Man','Grootverpakking','Vrouw'])
    content_recommendations()

    connection.commit()
    cursor.close()
    connection.close()

def collab_recommendations(segmentList,targetAudienceList):
    # Er bleek nog een probleem te zitten in mijn database ik had geen gender/target audience nog, als placeholder doe ik het type persoon
    # SELECT cart.products_id, cart.sessions_profiles_id, sessions.segment FROM cart
    # INNER JOIN sessions ON cart.sessions_profiles_id = sessions.browser_id
    # WHERE sessions.segment = 'BOUNCER' 
    # -- AND sessions.target_audience = 'familie'
    # AND sessions.segment IS NOT NULL
    for segment in segmentList:
        for target in targetAudienceList:
            sql = f"""
            SELECT DISTINCT cart.products_id, cart.sessions_profiles_id, sessions.segment, products.targetaudience, products.category, products.sub_category, products.sub_sub_category
            FROM cart
            INNER JOIN sessions ON cart.sessions_profiles_id = sessions.browser_id
            INNER JOIN products ON cart.products_id = products.id
            WHERE sessions.segment = '{segment}' 
            AND products.targetaudience = '{target}'
            AND sessions.segment IS NOT NULL
            ORDER BY cart.products_id ASC"""
            cursor.execute(sql)
            allSimilarBuyersAndProducts = cursor.fetchall()
            used = []
            recommendList = []
            for buyerTypeAndProduct in allSimilarBuyersAndProducts:
                category = ''
                if buyerTypeAndProduct[0] in used:
                    continue
                else:
                    if buyerTypeAndProduct[4]: #category
                        category = category+buyerTypeAndProduct[4]
                        if buyerTypeAndProduct[5]: #sub_category
                            category = category+buyerTypeAndProduct[5]
                            if buyerTypeAndProduct[6]: #sub_sub_category
                                category = category+buyerTypeAndProduct[6]

                    used.append(buyerTypeAndProduct[0])
                    recommendList.append(buyerTypeAndProduct[0])
                    if len(recommendList) == 4:
                        # Sorry voor de string manipulation
                        listString = str(recommendList).replace('[','{').replace(']','}').replace('\'','"')
                        insertSql = f"""INSERT INTO collab_recommendations 
                            (segment,target_audience,category,product_recommendation)
                            VALUES (%s,%s,%s,%s)"""
                        cursor.execute(insertSql,(segment,target,category,listString))
                        recommendList = []
    


def content_recommendations():
    sql = """SELECT p.id,p.name,p.category,p.sub_category,p.sub_sub_category, COUNT (cart.products_id)
            FROM products AS p
            INNER JOIN cart ON p.id = cart.products_id
            GROUP BY p.id,p.name,p.category,p.sub_category,p.sub_sub_category,cart.bought
            ORDER BY p.category,p.sub_category,p.sub_sub_category, COUNT(cart.products_id) DESC"""
    cursor.execute(sql)
    similarProducts = cursor.fetchall() #groupedby amount bought in order of category importance
    recommendList = []
    for product in similarProducts:
        if product[2]: #category
            category = product[2]
            if product[3]: #sub_category
                category = product[3]
                if product[4]: #sub_sub_category
                    category = product[4]
                    recommendList.append(product[0])

        if len(recommendList) == 4:
            # Sorry voor de string manipulation
            listString = str(recommendList).replace('[','{').replace(']','}').replace('\'','"')
            insertSql = f"""INSERT INTO content_recommendations 
                (category,product_recommendation)
                VALUES (%s,%s)"""
            recommendList = []
            cursor.execute(insertSql,(category,listString))