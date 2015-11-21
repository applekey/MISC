#### travel question
import csv, sqlite3
##class to generate a testing dataset
class testing:
    def generateDataSet(self):
        #hotel_name,nightly_rate,promo_txt,deal_value,deal_type,start_date,end_date
        str ='''Hotel Foobar,250,$50 off your stay 3 nights or more,-50,rebate_3plus,2016-03-01,2016-03-31 \n
        Hotel Foobar,250,5% off your stay,-5,pct,2016-03-01,2016-03-15 \n
        Hotel Foobar,250,$20 off your stay,-20,rebate,2016-03-07,2016-03-15 \n'''
        return str

##class that finds the deal given a dataset and a trip
class sqlLiteManager:
    def __init__(self, inMemory = False):
        self.connection = None
        self.inMemory = inMemory

    def CreateTable(self, columns):
        con = sqlite3.connect(":memory:")
        self.connection = con

        #create sql create table string
        sqlCreateTable = 'CREATE TABLE t ('

        for column in columns:
            sqlCreateTable += column + ','

        sqlCreateTable = sqlCreateTable[:-1] ## remove the last comma char
        sqlCreateTable += ');'
        print sqlCreateTable
        cur = con.cursor()
        cur.execute(sqlCreateTable)

    def InsertData(self, columnNames, data):
        if self.connection == None:
            # todo: throw some kind of error
            return

        values = '('
        columnString = '('
        for column in columnNames:
            columnString += column  + ','
            values += '?,'
        columnString = columnString[:-1]
        values = values [:-1]
        columnString += ')'
        values +=')'

        cur = self.connection.cursor()
        insertString = "INSERT INTO t" + columnString + "VALUES"+values +';'
        cur.executemany(insertString, data)
        self.connection.commit()


class findDeal:
    def __init__(self):
        self.dealTuple = []
        self.sqlLiteManager = sqlLiteManager()

    def parseDeals(self, dataSet, format):
        with open('travel.csv') as csvfile:
            dictrdr = csv.DictReader(csvfile)

            columns = dictrdr.fieldnames
            self.sqlLiteManager.CreateTable(dictrdr.fieldnames)

            for kk in dictrdr:
                print kk.values()
            #create dict for data
            to_db = [(i['hotel_name'], i['nightly_rate']) for i in dictrdr]

            self.sqlLiteManager.InsertData(columns,dictrdr)
            return

    def findDeal(self, dataset, trip):
        self.parseDeals(dataset,'csv')

def main():
    #generate testing dataset
    test = testing()
    dataset = test.generateDataSet()

    #parse deals
    dealFinder = findDeal()
    dealFinder.findDeal(dataset,'my trip')

main()
