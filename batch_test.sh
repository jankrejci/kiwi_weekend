#!/bin/bash
./book_flight.py  --date 2018-03-01 --from PRG --to LAX
./book_flight.py  --date 2018-03-27 --from STN --to MXP --fastest
./book_flight.py  --date 2018-03-14 --from ORD --to JFK --one-way
./book_flight.py  --date 2018-03-07 --from CDG --to ATL --cheapest
./book_flight.py  --date 2018-04-03 --from PEK --to LHR --bags 2
./book_flight.py  --date 2018-04-30 --from PEK --to LHR --bags 1 
./book_flight.py  --date 2018-04-11 --from PEK --to LHR --bags 0
./book_flight.py  --date 2018-04-17 --from BCN --to ARN --return 0
./book_flight.py  --date 2018-05-04 --from FCO --to DME --return 1
./book_flight.py  --date 2018-05-21 --from HEL --to PED --return 5
./book_flight.py  --date 2018-05-30 --from BRQ --to DXB --return 5 --bags 2 --fastest
./book_flight.py  --date 2018-05-30 --from BRQ --to DWC --one-way --bags 1 --cheapest
./book_flight.py  --date 2018-04-13 --from BCN --to DUB --one-way
./book_flight.py  --date 2018-04-13 --from LHR --to DXB --return 5
./book_flight.py  --date 2018-04-13 --from NRT --to SYD --cheapest --bags 2
./book_flight.py  --date 2018-04-13 --from CPH --to MIA --fastest
