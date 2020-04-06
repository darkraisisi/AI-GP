from pymongo import MongoClient
import csv
from datetime import datetime

envvals = ["MONGODBUSER", "MONGODBPASSWORD", "MONGODBSERVER", "RECOMADDRESS"]
dbstring = 'mongodb+srv://{0}:{1}@{2}/test?retryWrites=true&w=majority'

client = MongoClient()
database = client.huwebshop

def multi_getattr(obj, attr, default = None):
    """
    http://code.activestate.com/recipes/577346-getattr-with-arbitrary-depth/
    Source
    Changed it a tiny bit
    """
    attributes = attr.split(".")
    for i in attributes:
        try:
            obj = obj.get(i)
        except AttributeError:
            try:
                obj = obj[int(i)]
            except:
                return default
    return obj

def generateBrandsCSV(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        
        brandDict = {} #id:brandName
        for record in mongoCollections:
            c += 1
            try:
                brandDict.setdefault(record[mongoFieldNames[1]], len(brandDict)+1)
            except:
                brandDict.setdefault('None', len(brandDict)+1)
            if c % 10000 == 0:
                
                print(f"{c} records sorted...")

        for item in brandDict:
            writer.writerow({csvFieldNames[0]:brandDict[item],csvFieldNames[1]:item})

    print(f"Finished creating {fileNameString}")
    return brandDict

def generateCSVProducts(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames,brandDict):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        for record in mongoCollections:
            c+=1
            writeDict = {}
            for x in range(len(csvFieldNames)):
                if csvFieldNames[x] != 'brand':
                    writeDict.update({ csvFieldNames[x]: multi_getattr(record,mongoFieldNames[x]) })
                else:
                    brandId = brandDict.get(multi_getattr(record,mongoFieldNames[x]))
                    writeDict.update({ csvFieldNames[x]: brandId })
            writer.writerow(writeDict)
            if c % 10000 == 0:
                
                print(f"{c} records written...")

    print(f"Finished creating {fileNameString}")


def generateCSVProfiles(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        
        buidDict = {} #buid:profileId
        for record in mongoCollections:
            c += 1
            for buid in record.get('buids',[]):
                try:
                    buidDict.setdefault(buid, str(record[mongoFieldNames[0]]))
                except:
                    continue

            writeDict = {}
            for x in range(len(csvFieldNames)):
                writeDict.update({ csvFieldNames[x]: multi_getattr(record,mongoFieldNames[x]) })
            writer.writerow(writeDict)

            if c % 10000 == 0:
                
                print(f"{c} records sorted...")

    print(f"Finished creating {fileNameString}")
    return buidDict


def generateCSVSessions(fileNameString, mongoCollections, csvFieldNames, mongoFieldNames,buidDict):
    print(f"Creating the CVS for {fileNameString}...")
    sessionHasProductList = {}
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        for record in mongoCollections:
            c+=1
            writeDict = {}
            browserId = multi_getattr(record,mongoFieldNames[0],None)
            if None == browserId:
                continue
            else:
                try:
                    if(sessionHasProductList.get(browserId)):
                            sessionHasProductList[browserId]['cart'].append({'productList':multi_getattr(record,'order.products',[]), 'bought':int(multi_getattr(record,'has_sale',0) == True) })
                    else:
                        sessionHasProductList.update({browserId:{'cart':[]}})
                        sessionHasProductList[browserId]['cart'].append({'productList':multi_getattr(record,'order.products',[]), 'bought':int(multi_getattr(record,'has_sale',0) == True) })


                except TypeError:
                    if(sessionHasProductList.get(browserId[0])):
                        sessionHasProductList[browserId[0]]['cart'].append({'productList':multi_getattr(record,'order.products',[]), 'bought':int(multi_getattr(record,'has_sale',0) == True) })
                    else:
                        sessionHasProductList.update({browserId[0]:{'cart':[]}})
                        sessionHasProductList[browserId[0]]['cart'].append({'productList':multi_getattr(record,'order.products',[]), 'bought':int(multi_getattr(record,'has_sale',0) == True) })


            for x in range(len(csvFieldNames)):
                if csvFieldNames[x] != 'profiles_id':
                    writeDict.update({ csvFieldNames[x]: multi_getattr(record,mongoFieldNames[x]) })
                else:
                    tmp = writeDict[csvFieldNames[0]]
                    try:
                        profileId = buidDict.get(tmp,None)
                    except TypeError:
                        profileId = buidDict.get(tmp[0],None)
                    writeDict.update({ csvFieldNames[x]: profileId })
            writer.writerow(writeDict)

            if c % 10000 == 0:
                
                print(f"{c} records written...")
    print(f"Finished creating {fileNameString}")
    return sessionHasProductList


def generateCSVCart(fileNameString, sessionHasProductList, csvFieldNames, mongoFieldNames):
    print(f"Creating the CVS for {fileNameString}...")
    with open(fileNameString, 'w', newline='', encoding='utf-8') as csvout:
        writer = csv.DictWriter(csvout, fieldnames=csvFieldNames)
        writer.writeheader()
        c = 0
        for buid in sessionHasProductList:
            c+=1
            writeDict = {}
            writeDict.update({csvFieldNames[1]:buid})
            for carts in sessionHasProductList[buid]['cart']:
                writeDict.update({csvFieldNames[2]:carts[csvFieldNames[2]]})
                for product in carts['productList']:
                    writeDict.update({csvFieldNames[0]:product.get('id')})
                    writer.writerow(writeDict)
            
            if c % 10000 == 0:
                
                print(f"{c} records written...")
    print(f"Finished creating {fileNameString}")


def generateAllCSV():
    AbsoluteStartTime = datetime.now()
    startTime = datetime.now()

    products = database.products.find()
    brandDict = generateBrandsCSV('setup/csv/brand.csv', products,
    ['id','name'],
    ['','brand'])

    products = database.products.find()
    generateCSVProducts('setup/csv/products.csv', products,
    ['id','brand','name','targetaudience','category', 'sub_category','sub_sub_category','msrp','discount','sellingprice','deal'],
    ['_id','brand','name','gender','category', 'sub_category', 'sub_sub_category','price.mrsp','price.discount','price.selling_price','properties.discount'],
    brandDict)

    profiles = database.profiles.find()
    buids = generateCSVProfiles('setup/csv/profiles.csv', profiles,
    ['id', 'order_amount', 'latest', 'segment'],
    ['_id', 'order.count', 'latest_activity','recommendations.segment'])
    print(f'It took {datetime.now() - startTime} seconds to write the profiles.')

    startTime = datetime.now()
    sessions = database.sessions.find()
    sessionHasProductList = generateCSVSessions('setup/csv/sessions.csv', sessions,
    ['browser_id','profiles_id','segment','starttime','endtime','devicetype'],
    ['buid.0','profiles_id','segment','session_start','session_end','os.familiy'],
    buids)
    print(f'It took {datetime.now() - startTime} seconds to write the sessions')

    startTime = datetime.now()
    generateCSVCart('setup/csv/cart.csv', sessionHasProductList,
    ['product_id', 'sessions_profiles_id', 'bought'],
    ['sessions_profiles_id', 'bought'])
    print(f'It took {datetime.now() - startTime} seconds to write the carts.')
    print(f'It took {datetime.now() - AbsoluteStartTime} seconds to write all the csv\'s.')