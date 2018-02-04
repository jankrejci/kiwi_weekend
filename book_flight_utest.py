#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 16:37:35 2018

@author: jankrejci
"""

# TODO change module import
import sys
sys.path.append('/home/jankrejci/kiwi_weekend/')
import book_flight as bf
import unittest

#import importlib
#importlib.reload(book_flight)

class KnownValues(unittest.TestCase):
    # TODO adjust dates, airports and results
    parseArguments_known_values = (
        (
        # minimal variant
        ['--date', '2018-02-01', '--from', 'PRG', '--to', 'LAX'],
        {'flight_date' : '01/02/2018', 'dst_from' : 'PRG', 'dst_to' : 'LAX', 'one_way' : True, 'nights' : None, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
        (
        # fastest option
        ['--date', '2018-02-27', '--from', 'LON', '--to', 'MIL', '--fastest'],
        {'flight_date' : '27/02/2018', 'dst_from' : 'LON', 'dst_to' : 'MIL', 'one_way' : True, 'nights' : None, 'cheapest' : False, 'fastest' : True, 'bags' : 0}
        ),
        (
        # one way option (default)
        ['--date', '2018-02-14', '--from', 'CHI', '--to', 'JFK', '--one-way'],
        {'flight_date' : '14/02/2018', 'dst_from' : 'CHI', 'dst_to' : 'JFK', 'one_way' : True, 'nights' : None, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
        (
        # cheapest option (default)
        ['--date', '2018-02-07', '--from', 'CDG', '--to', 'ATL', '--cheapest'],
        {'flight_date' : '07/02/2018', 'dst_from' : 'CDG', 'dst_to' : 'ATL', 'one_way' : True, 'nights' : None, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
        (
        # two bags
        ['--date', '2018-03-03', '--from', 'PEK', '--to', 'LHR', '--bags', '2'],
        {'flight_date' : '03/03/2018', 'dst_from' : 'PEK', 'dst_to' : 'LHR', 'one_way' : True, 'nights' : None, 'cheapest' : True, 'fastest' : False, 'bags' : 2}
        ),
        (
        # just one bag
        ['--date', '2018-03-31', '--from', 'FRA', '--to', 'YSD', '--bags', '1'],
        {'flight_date' : '31/03/2018', 'dst_from' : 'FRA', 'dst_to' : 'YSD', 'one_way' : True, 'nights' : None, 'cheapest' : True, 'fastest' : False, 'bags' : 1}
        ),
        (
        # return the same day
        ['--date', '2018-03-17', '--from', 'BCN', '--to', 'MUC', '--return', '0'],
        {'flight_date' : '17/03/2018', 'dst_from' : 'BCN', 'dst_to' : 'MUC', 'one_way' : False, 'nights' : 0, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
        (
        # one night stay
        ['--date', '2018-04-04', '--from', 'FCO', '--to', 'DME', '--return', '1'],
        {'flight_date' : '04/04/2018', 'dst_from' : 'FCO', 'dst_to' : 'DME', 'one_way' : False, 'nights' : 1, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
        (
        # more night stay
        ['--date', '2018-04-21', '--from', 'HEL', '--to', 'PED', '--return', '5'],
        {'flight_date' : '21/04/2018', 'dst_from' : 'HEL', 'dst_to' : 'PED', 'one_way' : False, 'nights' : 5, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
        (
        # maximum options
        ['--date', '2018-04-30', '--from', 'BRQ', '--to', 'DXB', '--return', '5', '--bags', '1', '--fastest'],
        {'flight_date' : '30/04/2018', 'dst_from' : 'BRQ', 'dst_to' : 'DXB', 'one_way' : False, 'nights' : 5, 'cheapest' : False, 'fastest' : True, 'bags' : 1}
        ),
        (
        # maximum default options
        ['--date', '2018-04-09', '--from', 'WAW', '--to', 'BTS', '--one-way', '--bags', '0', '--cheapest'],
        {'flight_date' : '09/04/2018', 'dst_from' : 'WAW', 'dst_to' : 'BTS', 'one_way' : True, 'nights' : None, 'cheapest' : True, 'fastest' : False, 'bags' : 0}
        ),
    )


    def test_parseArguments_known_values(self):
        for debug_args, args in self.parseArguments_known_values:
            result = bf.parseArguments(debug_args)
            self.assertEqual(args, result)


if __name__ == '__main__' :
    unittest.main()