
from traveTest import *
import unittest, sys,os

sys.path.append('travel.py')
from travel import *

class TestTravel(unittest.TestCase):
    def cols(self):
        self.columns = ['hotel_name NVARCHAR(100)', 'nightly_rate INT', 'promo_txt NVARCHAR(100)', 'deal_value INT', 'deal_type NVARCHAR(100)', 'start_date DATETIME ', 'end_date DATETIME']

    def testBasic(self):
        self.cols()
        to_db = [['a', '250', 'fdsa', '-50', 'rebate_3plus', '2016-03-01', '2016-03-31'],
                    ['a', '250', 'fdsa', '-5', 'pct', '2016-03-01', '2016-03-15'],
                    ['a', '250', 'fdsa', '-20', 'rebate', '2016-03-07', '2016-03-15']]
        manager = DealManager(enableCache = True)
        manager.insertData(self.columns,to_db)

        #PARSE DEALS
        trip = 'a, 2016-03-5,3'
        tripArgs = parseInput (trip)
        answer = manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])
        self.assertEqual(answer, (700.0, 'fdsa'))

    def testRebate(self):
        self.cols()
        to_db = [['a', '250', 'rebate_3plus', '-50', 'rebate_3plus', '2016-03-01', '2016-03-31'],
                            ['b', '250', 'pct', '-5', 'pct', '2016-03-01', '2016-03-15'],
                            ['c', '250', 'rebate', '-20', 'rebate', '2016-03-07', '2016-03-15']]
        manager = DealManager(enableCache = True)
        manager.insertData(self.columns,to_db)

        #PARSE DEALS
        trip = 'a, 2016-03-5,3'
        tripArgs = parseInput (trip)
        answer = manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])
        self.assertEqual(answer, (700.0, 'rebate_3plus'))
    def testpct(self):
        self.cols()
        to_db = [['a', '250', 'rebate_3plus', '-50', 'rebate_3plus', '2016-03-01', '2016-03-31'],
                            ['b', '250', 'pct', '-5', 'pct', '2016-03-01', '2016-03-15'],
                            ['c', '250', 'rebate', '-20', 'rebate', '2016-03-07', '2016-03-15']]
        manager = DealManager(enableCache = True)
        manager.insertData(self.columns,to_db)

        #PARSE DEALS
        trip = 'b, 2016-03-5,3'
        tripArgs = parseInput (trip)
        answer = manager.BestDeal(tripArgs[0],tripArgs[1],tripArgs[2])
        self.assertEqual(answer, (787.5, 'pct'))

if __name__ == '__main__':
    unittest.main()
