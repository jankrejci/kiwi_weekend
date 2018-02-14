#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import requests
import argparse
import datetime


def parseArguments(debug_args = []):
    parser = argparse.ArgumentParser(
                description = 'Search and book flight on Kiwi.com',
                epilog = 'example usage:' + '\n' +
                         '  ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2 --return 5' + '\n',
                formatter_class = argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--date',
        dest = 'flight_date',
        required = True,
        help = 'flight departure date, format YYYY-MM-DD'
    )
    parser.add_argument(
        '--from',
        dest = 'dst_from',
        required = True,
        help = 'departure destination IATA code'
    )
    parser.add_argument(
        '--to',
        dest = 'dst_to',
        required = True,
        help = 'arrival destination IATA code'
    )
    group_way = parser.add_mutually_exclusive_group()
    group_way.add_argument(
        '--one-way',
        dest = 'one-way',
        default = True,
        action = 'store_true',
        help = 'one way ticket (default)'
    )
    group_way.add_argument(
        '--return',
        dest = 'return',
        type = int,
        help = 'return ticket with NIGHTS stayed in destination'
    )
    group_type = parser.add_mutually_exclusive_group()
    group_type.add_argument(
        '--cheapest',
        dest = 'cheapest',
        default = True,
        action = 'store_true',
        help = 'choose the cheapest ticket available'
    )
    group_type.add_argument(
        '--fastest',
        dest = 'fastest',
        default = False,
        action = 'store_true',
        help = 'choose the ticket with fastest flight'
    )
    parser.add_argument(
        '--bags',
        dest = 'bags',
        default = 0,
        type = int,
        choices = [0, 1, 2],
        help = 'number of bags, you want to carry (default = 0)'
    )
    parsed_args = {}
    if debug_args:
        parsed_args = vars(parser.parse_args(args=debug_args))
    else:
        parsed_args = vars(parser.parse_args())

    if  parsed_args['return'] != None:
        parsed_args['one-way'] = False

    if parsed_args['fastest']:
        parsed_args['cheapest'] = False

    try:
        parsed_args['flight_date'] = datetime.datetime.strptime(parsed_args['flight_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:
         print('error: wrong input of the date')
    # returns dictionary with parsed args
    return(parsed_args)


def createSearchParams(parsed_args):
    assert isinstance(parsed_args, dict)
    assert len(parsed_args) == 8
    flight_type = 'oneway'
    if not parsed_args['return'] == None:
        flight_type = 'return'
    search_params = {
        'v' : '3',
        'flyFrom' : parsed_args['dst_from'],
        'to' : parsed_args['dst_to'],
        'dateFrom' : parsed_args['flight_date'],
        'dateTo' : parsed_args['flight_date'],
        'typeFlight' : flight_type,
        'adults' : '1',
        'limit' : '10'
    }
    if not parsed_args['return'] == None:
        search_params['daysInDestinationFrom'] = str(parsed_args['return'])
        search_params['daysInDestinationTo'] = str(parsed_args['return'])
    return(search_params)


def searchFlights(search_params):
    assert isinstance(search_params, dict)

    url='https://api.skypicker.com/flights?'
    response = requests.get(url=url, params=search_params)
    flights = json.loads(response.text)
    return(flights['data'])


def cleanFlights(parsed_args, flights):
    clean_flights = []
    for flight in flights:
        flight_date = datetime.datetime.fromtimestamp(flight['dTime']).strftime('%d/%m/%Y')
        if flight_date != parsed_args['flight_date']:
            continue
        if len(flight['bags_price']) < parsed_args['bags']:            
            continue
        clean_flights.append(flight)
    return(clean_flights)

def chooseFlight(parsed_args, flights):
    assert isinstance(parsed_args, dict)
    assert len(parsed_args) == 8
    assert isinstance(flights, list)

    min_price = float('inf')
    min_duration = float('inf')
    selected_flight = {}
    for flight in flights:
        if len(flight['bags_price']) >= parsed_args['bags']:
            if parsed_args['cheapest']:
                bags_price = 0
                if parsed_args['bags'] > 0:
                    bags_price = flight['bags_price'][str(parsed_args['bags'])]
                total_price = flight['price'] + bags_price
                if total_price < min_price:
                    min_price = total_price
                    selected_flight = flight
            if parsed_args['fastest']:
                if flight['duration']['total'] < min_duration:
                    min_duration = flight['duration']['total']
                    selected_flight = flight
    return(selected_flight)


def createBookingPayload(parsed_args, selected_flight, default = True):
    assert isinstance(parsed_args, dict)
    assert len(parsed_args) == 8
    assert isinstance(selected_flight, dict)
    #TODO why the lengt is sometimes 32 and sometimes 33?
    assert len(selected_flight) >= 32
    
    booking_payload = {
        'lang' : 'en',
        'bags' : parsed_args['bags'],
        'locale' : 'en',
        'currency' : 'EUR',
        'booking_token' : selected_flight['booking_token'],
        'affily' : 'affilid',
        'booked_at' : 'affilid',
        'user_id' : 'sJmOzzndJQBGutKaL7nRz9',
        'secret_token' : '93bb1d9ad556bd4b52526ff505cfa4321473405206',
        'immediate_confirmation' : True
    }
    
    hold_bags = {}
    for id_number in selected_flight['id'].split(sep='|'):
        hold_bags[id_number] = {}
        for bag_count in range(1, 4):
            if bag_count == parsed_args['bags']:
                hold_bags[id_number][str(bag_count)] = 1
            else:
                hold_bags[id_number][str(bag_count)] = 0

    if default:
        booking_payload['passengers'] = [
                {
                 'documentID' : '12345',
                 'firstName' : 'John',
                 'lastName' : 'Snow',
                 'title' : 'Mr',
                 'phone' : '+44 44857282842',
                 'birthday' : '1985-04-21',
                 'expiration' : 1639958400,
                 'cardno' : 'K000007',
                 'nationality' : 'N',
                 'email' : 'john.snow@winterfell.com',
                 'category' : 'adults',
                 'hold_bags' : hold_bags
                },
        ]
    else:
        #TODO read data from config file
        pass
    return(booking_payload)


def bookFlight(booking_payload):
    url = 'http://128.199.48.38:8080/booking'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(booking_payload), headers=headers)
    booking_response = json.loads(response.text)
    return booking_response


def printResponse(response, parsed_args, selected_flight):
    assert isinstance(selected_flight, dict)
    if response['status'] == 'confirmed':
        print('Your flight has been confirmed')
        print('From:      ' + selected_flight['flyFrom'])
        print('To:        ' + selected_flight['flyTo'])
        departure = datetime.datetime.fromtimestamp(selected_flight['dTime']).strftime('%d/%m/%Y %H:%M')
        print('Departure: ' + departure)
        price = int(selected_flight['price'])
        if parsed_args['bags'] > 0:
            price += int(selected_flight['bags_price'][str(parsed_args['bags'])])
        print('Price:     ' + str(price) + ' EUR')
        print('Code:      ' + response['pnr'])
        print()
    else:
        print('ERROR your flight has not been confirmed.')
        print(response)
        print()
        

def main():
    parsed_args = parseArguments()
    search_params = createSearchParams(parsed_args)
    flights = searchFlights(search_params)
    selected_flight = chooseFlight(parsed_args, flights)
    if not selected_flight:
        print('ERROR no flight was found.')
        print('From:      ' + parsed_args['dst_from'])
        print('To:        ' + parsed_args['dst_to'])
        departure = parsed_args['flight_date']
        print('Departure: ' + departure)
        print()
        return 0
    booking_payload = createBookingPayload(parsed_args, selected_flight)
    response = bookFlight(booking_payload)
    printResponse(response, parsed_args, selected_flight)
    return(response['pnr'])


if __name__ == '__main__':
    main()
