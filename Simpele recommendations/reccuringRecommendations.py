import psycopg2
import csv
from datetime import datetime
import copy

# broken count
"""
SELECT s.profiles_id, s.browser_id, s.starttime, c.products_id,COUNT(c.products_id) FROM sessions AS s
INNER JOIN cart as c ON s.browser_id = c.sessions_profiles_id
WHERE s.profiles_id = '59ddc300a56ac6edb4ea36c1'
GROUP BY s.profiles_id, s.browser_id, s.starttime, c.products_id
-- ORDER BY s.profiles_id, s.browser_id, s.starttime
ORDER BY c.products_id
"""

# Intersting way of removing group by for broken count
"""
SELECT s.profiles_id, s.browser_id, s.starttime, c.products_id, COUNT(c.products_id) OVER() FROM sessions AS s
INNER JOIN cart as c ON s.browser_id = c.sessions_profiles_id
WHERE s.profiles_id = '59ddc300a56ac6edb4ea36c1'
-- GROUP BY s.profiles_id, s.browser_id, s.starttime, c.products_id
-- ORDER BY s.profiles_id, s.browser_id, s.starttime
ORDER BY c.products_id
"""

"""
SELECT s.profiles_id, s.browser_id, s.starttime, c.products_id FROM sessions AS s
INNER JOIN cart as c ON s.browser_id = c.sessions_profiles_id
WHERE s.profiles_id = '59ddc300a56ac6edb4ea36c1'
ORDER BY s.profiles_id, s.browser_id, s.starttime, c.products_id
"""

"""
1.  First get all products bought per specific user.
2.  See if there are some products that have been bought pultiple times.
3.  See if the time between same items bought is somewhat consistent.
        If this is true get the average time between purchases.
5.  Set in the database a product refrence, time_between, person_id.
        This way when a person returns to the home page we can serve them this reoccuring recommendation in a timely manner.
"""

def getProductReccurancetimeAllUser():
    connection = psycopg2.connect("dbname=OpisOp user=postgres password=root")
    cursor = connection.cursor()
    startTime = datetime.now()
    sql = """
    SELECT s.profiles_id, s.browser_id, s.starttime, c.products_id FROM sessions AS s
    INNER JOIN cart as c ON s.browser_id = c.sessions_profiles_id
    WHERE s.profiles_id IS NOT NULL
    ORDER BY s.profiles_id, s.browser_id, s.starttime, c.products_id
    """


    cursor.execute(sql)
    print("Selecting rows table using cursor.fetchall")
    records = cursor.fetchall()
    # print(records)

    currentUser = ''
    userRecurringOrder = {}
    for record in records:
        if(currentUser != record[0]):
            # different user, set currentuser and update the user with the current product 
            currentUser = record[0]
            userRecurringOrder.update({currentUser:{record[3]:{'amount':1,'latestTime':record[2] } } })
        else:
            # check if this product exist if so add 1 instead of overwriting
            product = userRecurringOrder[currentUser].get(record[3])
            if(product):
                
                if(record[2] != userRecurringOrder[currentUser][record[3]]['latestTime']):
                    timeBetween = record[2] - userRecurringOrder[currentUser][record[3]]['latestTime']
                    totalTime = userRecurringOrder[currentUser][record[3]].get('timeBetweenTotal')
                    if(totalTime):
                        timeBetweenTotal =  totalTime + timeBetween
                        userRecurringOrder[currentUser].update({record[3]:{'amount':product['amount']+1,'latestTime':record[2],'timeBetweenTotal':timeBetweenTotal } })
                    else:
                        userRecurringOrder[currentUser].update({record[3]:{'amount':product['amount']+1,'latestTime':record[2],'timeBetweenTotal':timeBetween } })
                
            else:
                userRecurringOrder[currentUser].update({record[3]:{'amount':1,'latestTime':record[2] } })

    print(f'This mess took{datetime.now() - startTime}seconds ,started {startTime}')    
    return userRecurringOrder      


def orderAndWriteRecurrance(userRecurringOrder,csvFieldNames,fileNameString):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        for profileId in userRecurringOrder:
            for productId in userRecurringOrder[profileId]:
                product = userRecurringOrder[profileId][productId]
                if(product['amount'] > 2 ): # The cutoff value for the amount a product had been bought in sucsession
                    AverageReturnTime = product['timeBetweenTotal']/product['amount']
                    writer.writerow({'profile_id':profileId,'product_id':productId,'average_return_time':AverageReturnTime,'amount_bought':product['amount']})

def writeToDatabase(fileName):
    c = psycopg2.connect("dbname=OpisOp user=postgres password=root")
    cur = c.cursor()

    with open(fileName, encoding='utf-8') as csvfile:
        print("Copying {}...".format(fileName))
        cur.copy_expert("COPY recurring_recommendations FROM STDIN DELIMITER ',' CSV HEADER", csvfile)
        c.commit()

    cur.close()
    c.close()


fileName = 'Simpele recommendations/csv/recurrance.csv'
# userRecurringOrder = getProductReccurancetimeAllUser()
# orderAndWriteRecurrance(userRecurringOrder,['profile_id','product_id','average_return_time','amount_bought'],fileName)
writeToDatabase(fileName)