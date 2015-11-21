#### travel question VINCENT M CHEN ####
# Assumptions: one deal per trip, deal must be avaliable at start of trip, you must stick with your deal, cannot switch
# Design:
#       sql-db-engine to do heavy lifting for searching all avaliable deals for timeframe
#       in-memory optimization to find best deal for applicable trip
#       lightweight lru cache to store most hit trips
#
# Summary of code:
#  LRUCACHE:
#    -> check cache if trip already queried
#  SQL:
#      select * from deals where dealStartDate < tripStartDate and dealEndDate > tripStartDate orderby deal_type
#  Memory:
#   -> group all deals deal_type, find best discout by deal
#   -> Find best deal type to use

import csv, sqlite3, sys, os
from datetime import datetime,timedelta
from itertools import groupby

class CACHE:
    def __init__(self, capacity):
        self.cap = capacity
        self.currentCount = 0
        self.dataCache = {}
        self.lruCount = {}

    def get(self, key):
        if key in self.dataCache:
            self.lruCount[key] = self.currentCount
            self.currentCount += 1
            return self.dataCache[key]
        return None

    def set(self, key, value):
        if len(self.dataCache) > self.cap:
            old_key = min(self.lruCount.keys(), key=lambda k:self.lruCount[k])
            self.dataCache.pop(old_key)
            self.lruCount.pop(old_key)

        self.dataCache[key] = value
        self.lruCount[key] = self.currentCount
        self.currentCount += 1

##class that finds the deal given a dataset and a trip
class Logging:
    @staticmethod
    def Log(self, level, message, exceptionObject):
        ## dummy logging function
        pass

### Low level, generic sqllite manager
class sqlLiteManager:
    def __init__(self, dbName = None):
        self.connection = None
        self.dbName = dbName

    def Connect(self):
        try:
            if self.dbName == None: ## in memory db
                con = sqlite3.connect(":memory:")
            else:
                con = sqlite3.connect(self.dbName) # ":memory:"
            self.connection = con
        except ex:
            Logging.Log(1,'Cannot connect to DB',ex)
            raise Exception('Cannot connect to DB')

    def TableExist(self, name):
        if self.connection == None:
            # todo: throw some kind of error
            Logging.Log(1,'No DB connection for table exists.')
            return False

        querry ="SELECT name FROM sqlite_master WHERE type='table' AND name='"+name+  "';"
        #print querry
        try:
            c = self.connection.cursor()
            rtn = c.execute(querry)
        except ex:
            Logging.Log(2,'Table Exist Querry.Exception' ,ex)
            raise Exception('Table Exist Querry Exception ')

        found = False
        for row in rtn:
            found = True
        return found

    def CreateTable(self, name, columns):
        if self.connection == None:
            # todo: throw some kind of error
            Logging.Log(1,'No DB connection for create table.')
            return

        #create sql create table string
        sqlCreateTable = 'CREATE TABLE ' + name + ' ('

        for column in columns:
            sqlCreateTable += column + ','

        sqlCreateTable = sqlCreateTable[:-1] ## remove the last comma char
        sqlCreateTable += ');'
        #print sqlCreateTable
        try:
            cur = self.connection.cursor()
            cur.execute(sqlCreateTable)
        except ex:
            Logging.Log(2,'Create Table Exception' ,ex)
            raise Exception('Create Table Exception')

    def InsertData(self, name, columnNames, data):
        if self.connection == None:
            Logging.Log(2,'Insert Data No connection')
            return

        columnNames = [col.split(' ')[0] for col in columnNames]

        values = '('
        columnString = '('
        for column in columnNames:
            columnString += column  + ','
            values += '?,'
        columnString = columnString[:-1]
        values = values [:-1]
        columnString += ')'
        values +=')'

        insertString = "INSERT INTO " + name+' ' + columnString + "VALUES "+values +';'

        try:
            cur = self.connection.cursor()
            cur.executemany(insertString, data)
            self.connection.commit()
        except ex:
            Logging.Log(2,'Insert Data Exception' ,ex)
            raise Exception('Insert Exception')

    def executeQuerry(self,querry):
        if self.connection == None:
            # todo: throw some kind of error
            return None
        try:
            c = self.connection.cursor()
            result = c.execute(querry)
        except ex:
            Logging.Log(2,'Execute Exception:' + querry,ex)
            raise Exception('Execute Querry Exception')
        return result

### This class finds all deals that applicable to a trip
### This class does not optimize the deals
class findDealAdapter:
    def __init__(self):
        self.dealTuple = []
        self.sqlLiteManager = sqlLiteManager()
        self.sqlLiteManager.Connect()
        self.tableName = 'deals'
        self.defineColumnNames()

    def defineColumnNames(self):
        self.hotelName = 'hotel_name'
        self.nightlyRate = 'nightly_rate'
        self.promoTxt = 'promo_txt'
        self.deal_value = 'deal_value'
        self.deal_type = 'deal_type'
        self.start_date = 'start_date'
        self.end_date = 'end_date'

    def insertDeals(self, columns, dataSet, format):
        if not self.sqlLiteManager.TableExist(self.tableName):
            self.sqlLiteManager.CreateTable(self.tableName, columns)
            #create an index on hotelName
            indexCreate = 'CREATE INDEX hotelIndex ON '+ self.tableName +'(' +self.hotelName+');'
            self.sqlLiteManager.executeQuerry(indexCreate)

        self.sqlLiteManager.InsertData(self.tableName, columns,dataSet)

    def findDealBetweenTime(self, hotelName, checkInDate, endDate):
        querryColumns = [self.nightlyRate, self.promoTxt,self.deal_type,self.deal_value]
        querryColumns = ",".join(querryColumns)
        querryString = "select "+ querryColumns+" from deals where hotel_Name = '"+hotelName + "'" \
                        + 'and ' + "start_date<'" + str(checkInDate.strftime("%Y-%m-%d")) + "'and end_date>'"\
                        + str(checkInDate.strftime("%Y-%m-%d")) + "' ORDER BY " +self.deal_type+ " ;"

        queryResult =  self.sqlLiteManager.executeQuerry(querryString)

        results = []
        for row in queryResult:
            results.append([str(i) for i in list(row)])
        return results;

### This class optimizes the avaliable deals that are applicapble given a
## certain timeframe
class DealManager:
    def __init__(self, enableCache = True):
        self.cityCache = CACHE(100)
        self.dealFinder = findDealAdapter()
        self.dirty = False
        self.enableCache = enableCache
        ## caching diagnosis
        self.operations = 0
        self.operationsThatHitCache = 0

    def insertData(self, columns, to_db):
        self.dealFinder.insertDeals(columns, to_db,'csv')
        self.dirty = True
        self.cityCache = CACHE(100)

    def CheckIfCached(self,hotelName, start_date, duration):
        if self.dirty == True:
            return None

        if hotelName in self.cityCache.dataCache:
            city = self.cityCache.dataCache[hotelName]
            if start_date in city.dataCache:
                print 'Cache Hit'
                return city.dataCache[start_date]
        return None

    def CacheBestDeals(self, hotelName, date, bestDeals):
        if hotelName in self.cityCache.dataCache:
            self.cityCache.dataCache[hotelName].set(date,bestDeals)
        else:
            hotelDateCache = CACHE(1000)
            hotelDateCache.set(date,bestDeals)
            self.cityCache.set(hotelName,hotelDateCache)

    def BestDeal(self, hotelName, start_date,endDate):
        self.operations += 1
        duration = abs((endDate - start_date).days)
        if self.enableCache:
            cached = self.CheckIfCached(hotelName,start_date,endDate)
            if cached != None:
                self.operationsThatHitCache += 1
                return self.optimizeAvaliableDeals(hotelName,start_date,cached,duration,True)
        ### not in cache
        avaliableDeals = self.dealFinder.findDealBetweenTime(hotelName,start_date,endDate)
        results = self.optimizeAvaliableDeals(hotelName,start_date,avaliableDeals,duration,False)
        self.dirty = False
        return results

    ## reduced: from cache, already reduced just find min
    def optimizeAvaliableDeals(self, hotelName,start_date, avaliableDeals, duration, reduced = False):
        if avaliableDeals == None :
            return 'None'

        notFound = ('*', 'no deal available')
        #pct percentage
        #rebate
        #rebase, 3 nits or more
        bestPrice = (sys.maxint , '')
        #get the best discount, based on type
        if not reduced:
            groups = ([list(j) for i, j in groupby(avaliableDeals,lambda x: x[2])])
        else:
            groups = avaliableDeals

        if len(groups)!= 0 and self.enableCache:
            self.CacheBestDeals(hotelName,start_date,groups)

        if groups == None or len(groups) == 0:
            return notFound

        found = False
        for group in groups:
            bestOptionForType =  min(group,key=lambda x:float(x[3]))
            # check which kind it is
            beforeDiscount = duration * float(bestOptionForType[0])
            if bestOptionForType[2] == 'pct':
                totaPrice = beforeDiscount * (100.0 - float(bestOptionForType[3]))/100.0
                found = True
            elif bestOptionForType[2] == 'rebate_3plus' and duration >= 3:
                totaPrice = beforeDiscount - abs(float(bestOptionForType[3]))
                found = True
            elif bestOptionForType[2] == 'pct':
                totaPrice = beforeDiscount - abs(float(bestOptionForType[3]))
                found = True

            if found:
                if bestPrice[0] > totaPrice:
                    bestPrice = (totaPrice,bestOptionForType[1])
            else:
                bestPrice = notFound
        return bestPrice
########################################################################################

def parseParms(mInput):
    parms = mInput.split(',')
    hotelName = parms[0]
    checkInDate = parms[1].replace(' ','')
    duration = int(parms[2].replace(' ',''))
    checkInDate = datetime.strptime(checkInDate , '%Y-%m-%d')
    checkOutDate = checkInDate +timedelta(days=duration)
    return (hotelName,checkInDate,checkOutDate,duration)

def parseCSV(csvData):
    with open(csvData) as csvfile:
        dictrdr = csv.DictReader(csvfile)
        columns = dictrdr.fieldnames
        to_db = [[i[col] for col in columns] for i in dictrdr]
    return to_db, columns

def parseInput(inputArgs):
    args  = len(inputArgs)
    if not args ==  5:
        print 'Invalid format, it should be : BestHotelDeal ./deals.csv "Hotel Foobar" 2016-03-14 3'
        exit()
    args = list(sys.argv)

    args = args[1:]
    csvFileName = args[0]
    args = args[1:]

    ## test for duration
    try:
        duration = str(args[2])
        if int(duration) <= 0:
            print 'invalid duration'
            exit()
    except:
        print 'duration must be an int'
        exit()

    ## test to see if datetime is correct format
    dateInput = args[1]
    try:
        d = datetime.strptime(dateInput, "%Y-%m-%d")
    except:
        print 'invalid date time format'
        exit()

    ## test for csv exist
    if not os.path.isfile(csvFileName):
        print 'csv File name not exist'
        exit()

    trip = ",".join(args)
    return csvFileName,trip

if __name__ == '__main__':
    csvFileName,trip = parseInput(sys.argv)

    #READ IN DEALS
    to_db,columns = parseCSV(csvFileName)
    manager = DealManager(enableCache = True)
    manager.insertData(columns,to_db)

    #PARSE DEALS
    tripArgs = parseParms (trip)

    #FIND THE BEST DEAL
    print manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])[1]

    ## some code to test cache hit/miss
    # print manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])
    # print manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])
    # manager.insertData(columns,to_db)
    # print manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])
