#!/usr/bin/env python
#pylint: disable-msg=C0301,C0103

"""
Unit test for DAS QL parser
"""

import time
import unittest
from DAS.core.das_parser import add_spaces, parser
from DAS.core.das_parser import find_das_operator, find_das_word
from DAS.core.das_ql import das_operators

class testQLParser(unittest.TestCase):
    """
    A test class for the DAS qlparser
    """
    def setUp(self):
        """Initialization of unit test parameters"""
        self.daskeys   = ['file', 'site', 'lat', 'lon', 'date']
        self.operators = ['!=', '<=', '>=', '=']

    def test_add_spaces(self):
        """Test add_spaces function"""
        expr   = "a   <=1 b>1 c=1 d!=-1"
        expect = "a <= 1 b > 1 c = 1 d != -1"
        result = add_spaces(expr)
        self.assertEqual(expect, result)

    def test_parser(self):
        """Test parser function"""
        query  = "file lat site = New York"
        expect = {'fields':['file', 'lat'], 'spec':{'site':'New York'}}
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

        query  = "site=New York"
        expect = {'fields':None, 'spec':{'site':'New York'}}
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

        query  = "lat=1 file in [1,2]"
        expect = {'fields':None, 'spec':{'lat':1,'file':{'$in':[1,2]}}}
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

        query  = "lat=1 file between [1,2]"
        expect = {'fields':None, 'spec':{'lat':1,'file':{'$lte': 2, '$gte': 1}}}
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

    def test_parser2(self):
        """Test parser function w/ filters"""
        query  = "lon=1 | grep lon.name | sum(lon.name)"
        expect = {'fields':None, 'spec':{'lon':1}, 
                  'filters':['lon.name'],
                  'aggregators':[('sum', 'lon.name')]}
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

    def test_parser3(self):
        """Test parser function w/ time stamps"""
        query  = "lon=1 date last 24h"
        date1  = time.time() - 24*60*60
        date2  = time.time()
        expect = {'fields':None, 
                  'spec':{'lon':1, 'date': [long(date1), long(date2)]}} 
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

        query  = "lon=1 date=20100309"
        expect = {'fields':None, 'spec':{'lon':1, 'date': 20100309}} 
        result = parser(query, self.daskeys, self.operators)
        self.assertEqual(expect, result)

        query  = "lon=1 date= Sep 1 2010"
        self.assertRaises(Exception, parser, (query, self.daskeys, self.operators))

#
# main
#
if __name__ == '__main__':
    unittest.main()
