#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 16:37:35 2018

@author: jankrejci
"""

# TODO change module import
import sys
#sys.path.append('/home/jankrejci/kiwi_weekend/')
sys.path.append('c:\Krejci\gdrive\projekty\spyder\kiwi_weekend')

import datetime
import book_flight as bf
import unittest


class KnownValues(unittest.TestCase):
    '''unittest is not working with metropolitean IATA codes like LON, CHI, MIL, ...'''
    year = 2018
    month = 3
    multiple_input = (
        # minimal variant
        {'year':year, 'month':(month), 'day':1, 'from':'PRG', 'to':'LAX'},
        #fastest option
        {'year':year, 'month':(month), 'day':27, 'from':'STN', 'to':'MXP', 'fastest':True},
        # one way option (default)
        {'year':year, 'month':(month), 'day':14, 'from':'ORD', 'to':'JFK', 'one-way':True},
        # cheapest option (default)
        {'year':year, 'month':(month), 'day':7, 'from':'CDG', 'to':'ATL', 'cheapest':True},
        # two bags
        {'year':year, 'month':(month + 1), 'day':3, 'from':'PEK', 'to':'LHR', 'bags':2},
        # one bag (default) #TODO is one bag really default???
        {'year':year, 'month':(month + 1), 'day':30, 'from':'PEK', 'to':'LHR', 'bags':1},
        # no bags
        {'year':year, 'month':(month + 1), 'day':11, 'from':'PEK', 'to':'LHR', 'bags':0},
        # return the same day #TODO is it really needed to return the same day
        {'year':year, 'month':(month + 1), 'day':17, 'from':'BCN', 'to':'ARN', 'return':0},
        # one night stay
        {'year':year, 'month':(month + 2), 'day':4, 'from':'FCO', 'to':'DME', 'return':1},
        # more nights stay
        {'year':year, 'month':(month + 2), 'day':21, 'from':'HEL', 'to':'PED', 'return':5},
        # maximum options
        {'year':year, 'month':(month + 2), 'day':30, 'from':'BRQ', 'to':'DXB', 'return':5, 'bags':2, 'fastest':True},
        # maximum defaultoptions
        {'year':year, 'month':(month + 2), 'day':30, 'from':'BRQ', 'to':'DWC', 'one-way':True, 'bags':1, 'cheapest':True},
        # kiwi no.1
        #TODO departure next day ???
        {'year':2018, 'month':4, 'day':13, 'from':'BCN', 'to':'DUB', 'one-way':True},
        # kiwi no.2
        {'year':2018, 'month':4, 'day':13, 'from':'LHR', 'to':'DXB', 'return':5},
        # kiwi no.3
        #TODO departure next day ???
        {'year':2018, 'month':4, 'day':13, 'from':'NRT', 'to':'SYD', 'cheapest':True, 'bags':2},
        # kiwi no.4
        {'year':2018, 'month':4, 'day':13, 'from':'CPH', 'to':'MIA', 'fastest':True},
    )  
    
    single_input = (
        {'year':year, 'month':(month + 1), 'day':30, 'from':'PEK', 'to':'LHR', 'bags':1},
    )

    simple_input = multiple_input
#    simple_input = single_input
    
    instance_setup = False
    
    input_args = []
    parsed_args = []
    search_params = []
    search_results = []
    selected_flights = []
    booking_payloads = []
    responses = []
    
    
    def createInputArgs(self, simple_input):
        '''helper function automatize creation of input arguments'''
        input_values = []
        # mandatory values
        input_values.append('--date')
        input_values.append(str(simple_input['year']) + '-' + 
                            str(simple_input['month']).zfill(2) + '-' +
                            str(simple_input['day']).zfill(2))
        input_values.append('--from')
        input_values.append(simple_input['from'])
        input_values.append('--to')
        input_values.append(simple_input['to'])
        # optional values
        keys = ['fastest', 'cheapest', 'one-way']
        for key in keys:
            if key in simple_input:
                if simple_input[key]:
                    input_values.append('--' + key)
        # optional with parameter
        keys = ['return', 'bags']
        for key in keys:
            if key in simple_input:
                if simple_input[key] != None:
                    input_values.append('--' + key)
                    input_values.append(str(simple_input[key]))
        return(input_values)

   
    def createParsedArgs(self, simple_input):
        '''helper function automatize creation of parsed args'''
        parsed_args = {}
        # mandatory values
        parsed_args['flight_date'] = str(simple_input['day']).zfill(2) + '/' + \
                                     str(simple_input['month']).zfill(2) + '/' + \
                                     str(simple_input['year'])
        parsed_args['dst_from'] = simple_input['from']
        parsed_args['dst_to'] = simple_input['to']    
        # optional values, specified default values
        keys = (            
            ('cheapest', True),
            ('fastest' , False),
            ('one-way' , True),
            ('return'  , None),
            ('bags'    , 0)
        )
        for key, default_value in keys:
            if key in simple_input:
                parsed_args[key] = simple_input[key]  
                if key == 'fastest' and simple_input[key] == True:
                    parsed_args['cheapest'] = False
                if key == 'return' and simple_input[key] != None:
                    parsed_args['one-way'] = False
            else:
                parsed_args[key] = default_value
                
        return(parsed_args)
    
    
    def createSearchParams(self, parsed_args):
        '''helper function automatize creation of search params'''
        search_params = {}
        # mandatory values
        search_params['v'] = '3'
        search_params['adults'] = '1'
        search_params['limit'] = '10'
        date =  str(parsed_args['day']).zfill(2) + '/' + \
                str(parsed_args['month']).zfill(2) + '/' + \
                str(parsed_args['year'])
        search_params['dateFrom'] = date
        search_params['dateTo'] = date
        search_params['flyFrom'] = parsed_args['from']
        search_params['to'] = parsed_args['to']    
        # optional values, specified default values
        search_params['typeFlight'] = 'oneway'
        if 'return' in parsed_args:
            if parsed_args['return'] != None:
                search_params['typeFlight'] = 'return'
                search_params['daysInDestinationFrom'] = str(parsed_args['return'])
                search_params['daysInDestinationTo'] = str(parsed_args['return'])
        return(search_params)
            
            
    def setUpInstance(self):
        print('instance setup')
        for simple_input in self.simple_input:           
            self.input_args.append(self.createInputArgs(simple_input))
            self.parsed_args.append(self.createParsedArgs(simple_input))
            self.search_params.append(self.createSearchParams(simple_input))
    
    
    def setUp(self):
        if not self.instance_setup:
            self.setUpInstance()
            self.instance_setup = True
    
    
    def parseArguments_known_values(self):
        for input_args, parsed_args in zip(self.input_args, self.parsed_args):
            result = bf.parseArguments(input_args)
            self.assertEqual(parsed_args, result)
            
            
    def createSearchParams_known_values(self):
        for parsed_args, search_params in zip(self.parsed_args, self.search_params):
            result = bf.createSearchParams(parsed_args)
            self.assertEqual(search_params, result)
            
    
    def searchFlights_known_values(self):
        for search_params in self.search_params:            
            self.search_results.append(bf.searchFlights(search_params))
            for flight in self.search_results[-1]:
                input_params = []
                flight_params = []
                input_params.append(search_params['flyFrom'])
                flight_params.append(flight['flyFrom'])
                input_params.append(search_params['to'])
                flight_params.append(flight['flyTo'])
                input_params.append(search_params['typeFlight'])
                if flight['duration']['return'] == 0:
                     flight_params.append('oneway')
                else:
                     flight_params.append('return')
                self.assertEqual(input_params, flight_params)
        global GL_search_results
        GL_search_results = self.search_results

    
    def cleanFlights_known_values(self):
        # dTime - 1, because there are returned also flights at 00:00 next day 
        # TODO why server returns flights with day+1 date? is the UTC correct?
        self.clean_results = []
        for parsed_args, flights in zip(self.parsed_args, self.search_results):
            self.clean_results.append(bf.cleanFlights(parsed_args, flights))
            for flight in self.clean_results[-1]:
                flight_date = (datetime.datetime.fromtimestamp(flight['dTime']).strftime('%d/%m/%Y'))
                self.assertEqual(flight_date, parsed_args['flight_date'])
                self.assertGreaterEqual(len(flight['bags_price']), parsed_args['bags'])
        global GL_clean_results
        GL_clean_results = self.clean_results
 
           
    def chooseFlight_known_values(self):
        for parsed_args, flights in zip(self.parsed_args, self.clean_results):
            self.selected_flights.append(bf.chooseFlight(parsed_args, flights))
            if not self.selected_flights[-1]:
                continue
            global GL_parsed_args
            GL_parsed_args = parsed_args
            self.assertGreaterEqual(len(self.selected_flights[-1]['bags_price']), parsed_args['bags'])
            if parsed_args['cheapest']:
                bags_price = 0;
                if parsed_args['bags'] > 0:
                    bags_price = self.selected_flights[-1]['bags_price'][str(parsed_args['bags'])]
                selected_price = self.selected_flights[-1]['price'] + bags_price
                for flight in flights:
                    if len(flight['bags_price']) != parsed_args['bags']:
                        continue
                    bags_price = 0;
                    if len(flight['bags_price']) > 0:
                        bags_price = flight['bags_price'][str(parsed_args['bags'])]
                    flight_price = flight['price'] + bags_price
                    self.assertLessEqual(selected_price, flight_price)
            if parsed_args['fastest']:
                selected_duration = self.selected_flights[-1]['duration']['total']
                for flight in flights:
                    if len(flight['bags_price']) != parsed_args['bags']:
                        continue
                    self.assertLessEqual(selected_duration, flight['duration']['total'])
    
    
    def createBookingPayload_known_values(self):
        for parsed_args, selected_flight in zip(self.parsed_args, self.selected_flights):
            if len(selected_flight) < 32:
                print(parsed_args)
                print('ERROR no flight found.')
                print()
                continue
            self.booking_payloads.append(bf.createBookingPayload(parsed_args, selected_flight))
            self.assertEqual(len(self.booking_payloads[-1]), 11)
            
    
    def bookFlight_known_values(self):
        for booking_payload in self.booking_payloads:
            self.responses.append(bf.bookFlight(booking_payload))
        global GL_responses
        GL_responses = self.responses
    

    def printResponse_known_values(self):
        for response, parsed_args, selected_flight in zip(self.responses, self.parsed_args, self.selected_flights):
            if not selected_flight:
                continue
            print(parsed_args)
            bf.printResponse(response, parsed_args, selected_flight)
            
        
    def test_booking_known_values(self):
        '''monolithic test of all functions in defined order'''
        self.parseArguments_known_values()
        self.createSearchParams_known_values()
        self.searchFlights_known_values()
        self.cleanFlights_known_values()
        self.chooseFlight_known_values()
        self.createBookingPayload_known_values()
        self.bookFlight_known_values()
        self.printResponse_known_values()

    
if __name__ == '__main__' :
    unittest.main()
