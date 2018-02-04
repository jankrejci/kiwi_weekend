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
                       '  ./book_flight.py --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2 --return 5',
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
        dest = 'one_way',
        default = True,
        action = 'store_true',
        help = 'one way ticket (default)'
    )
    group_way.add_argument(
        '--return',
        dest = 'nights',
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
    # TODO input errors
    if debug_args:
        args = parser.parse_args(args=debug_args)
    else:
        args = parser.parse_args()

    if not args.nights == None:
        args.one_way = False

    if args.fastest:
        args.cheapest = False

    try:
        args.flight_date = datetime.datetime.strptime(args.flight_date, '%Y-%m-%d').strftime('%d/%m/%Y')
    except ValueError:
         print('error: wrong input of the date')
    # returns dictionary with parsed args
    return(vars(args))


def createSearchParams(args):
    assert isinstance(args, dict)
    assert len(args) == 8
    flight_type = 'oneway'
    if args['nights']:
        flight_type = 'return'
    search_params = {
        'v' : 3,
        'flyFrom' : args['dst_from'],
        'to' : args['dst_to'],
        'dateFrom' : args['flight_date'],
        'dateTo' : args['flight_date'],
        'typeFlight' : flight_type,
        'adults' : '1',
        'limit' : '60'
    }
    if not args['nights'] == None:
        search_params['daysInDestinationFrom'] : args['nights']
    return search_params


def searchFlights(search_params):
    assert isinstance(search_params, dict)

    url='https://api.skypicker.com/flights?'
    response = requests.get(url=url, params=search_params)
    flights = json.loads(response.text)
    return flights['data']


def chooseFlight(args, flights):
    assert isinstance(args, dict)
    assert len(args) == 8
    assert isinstance(flights, list)

    min_price = float('inf')
    min_duration = float('inf')
    selected_flight = []
    for flight in flights:
        if len(flight['bags_price']) >= args['bags']:
            if args['cheapest']:
                if flight['price'] < min_price:
                    min_price = flight['price']
                    selected_flight = flight
            if args['fastest']:
                if flight['duration']['total'] < min_duration:
                    min_duration = flight['duration']['total']
                    selected_flight = flight
    return selected_flight


def createPassengerCredentials(args):
    assert isinstance(args, dict)
    assert len(args) == 8

    default = True
    passenger_credentials = {}
    if default:
        passenger_credentials = {
                'lang':'en',
                'bags':args['bags'],
                'passengers' :

        }
    return passenger_credentials


def createBookingPayload(selected_flight, passenger_credentials):
    booking_payload = {}
    return booking_payload


def bookFlight(booking_payload):
    url = 'http://128.199.48.38:8080/booking'
    headers = {'content-type': 'application/json'}

    payload = {
        'lang' : 'en',
        'bags' : 2,
        'passengers' : [
                {
                'documentID' : '12345',
                'firstName' : 'John',
                'lastName' : 'Snow',
                'title' : 'Mr',
                'phone' : '+44 44857282842',
                'birthday' : '1985-04-21',
                'expiration' : 1639958400,
                'cardno' : 'D25845222',
                'nationality' : 'SE',
                'email' : 'email.address@gmail.com',
                'category' : 'infants',
                'hold_bags' : {
                        '341202495' : {
                                '1' : 1,
                                '2' : 0,
                                '3' : 0
                        },
                        '341214132' : {
                                '1' : 1,
                                '2' : 0,
                                '3' : 0
                        }
                }
                }
        ],
        'locale' : 'en',
        'currency' : 'EUR',
        'booking_token' : 'TjFsU9KOyjpEDqm5dNSrO1ZjuRMVMgZrERrSppD325T6P8+P9w468E+3gYirNKm0xjFEaQ8brFkJXYHcFnHHQP5fINbkDjCTreeWig4WZ7B4fBYYSUgmpu0Cq8+F75sB1L9aQ+cDGm5LObGbRYN0pwUDk5LuVOHkDPT1Qmo6XhmrtXw4mLqlylxVlpY+8jS2/eBYqLA7CPIQyfcUqPhx/F26+QR/TnuLRGUvd7cpYS88pyKmqcUiqIMz9FvuwQTxaTrPz8tES/e8I0br2Ukn4YrIvIX3jo30Rxwts1D64ZSjKrZne87kU+PYeizs0RTIYiVu5Zux/kNlWRTw4GuQENl5maQY+cvTyNeEmsSFNAnncJjC9hZeaAE665S2m17ZkQoH5qOydbZF321QBC3qXDzTZS6JFct/tS48NzvLd9u9vfull8wo3cBVl29GyOpSjdY+NJ3UzagFZOpNCT+tjIgElPELVzuzMAy7sqqvGk5b0SAO0D+xBuiOg3NIggZfHyZ+clsgRcMiTj33hVaSuL9PLtkvHV3xMgufu6AdAnVUQdv4qsWH3S4aXckyEVSpuVH1VxzYPm1ikRrUSup8lV/xJsITBR6v/IlkwTuWn6S4oasaojMW6sjrPrZObC0xtQ7jZ53BYcnYD+RGXeT6pTBfWjjjlgq45g5Hi2ta9fo=',
        'affily' : 'affilid',
        'booked_at' : 'affilid',
        'user_id' : 'sJmOzzndJQBGutKaL7nRz9',
        'secret_token' : '93bb1d9ad556bd4b52526ff505cfa4321473405206',
        'immediate_confirmation' : False
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(response['pnr'])


def main(debug_args = []):
    args = []
    if debug_args:
        args = parseArguments(debug_args)
    else:
        args = parseArguments()
    params = createSearchParams(args)
    flights = searchFlights(params)
    selected_flight = chooseFlight(args, flights)


if __name__ == '__main__':
    # TODO comment out debuging arguments and change parser method
    debug = True
    if debug:
        debug_args = [
                '--date', '2018-04-21',
                '--from', 'PRG',
                '--to', 'LON',
                '--fastest'
        ]
        main(debug_args)
    else:
        main()







