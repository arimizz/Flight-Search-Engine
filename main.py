from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager
import pprint

flight_search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
notification_manager = NotificationManager()


ORIGIN_CITY_IATA = "TLV"

#if the google sheets has the code of the city if it doesnt this loop will find the code for it.
city_has_code = True
# pprint.pprint(sheet_data)
#looping for the data in sheet data
for city in sheet_data:
    #if the part in the sheet data with the iatacode is empty  then make the trigger false
    if city["iataCode"] == "":
        city_has_code = False
    #if atleast one of the codes are empty break the loop. it means we need to find the code.
    if city_has_code == False:
        break

#if it broke the loop it means were missing a code so were making a list of the names of the cities.
if city_has_code == False:
    #make a list with all the city names
    city_names = [city["city"] for city in sheet_data]
    # print(city_names)
    #bring the code of the city's and store it in city_codes which is a dict
    city_codes = flight_search.get_destination_codes(city_names)
    #pass city code to the google sheet for it to update
    data_manager.update_destination_codes(city_codes)
    #after passing to google sheet make sheet_data have new data
    sheet_data = data_manager.get_destination_data()

# pprint.pprint(sheet_data)

#make a dict with code_name as key and id,city,lowest price as value
#dict comprenhsion
destinations = {
    sheet_data["iataCode"]: {
        "id":sheet_data["id"],
        "city":sheet_data["city"],
        "price":sheet_data["lowestPrice"]
        #for every row in sheet data put in the dict the code as key and the rest as values
    } for sheet_data in sheet_data}
# pprint.pprint(destinations)

#look for a flight from tomorrow which is today + 1
tomorrow = datetime.now() + timedelta(days=1)
#today + 6 days * 30 which is 6 months
six_month_from_today = datetime.now() + timedelta(days=6 * 30)


#for every code in the destination dict check if theres a cheaper flight
for city_code,dict in destinations.items():
    #searches for flight from tlv to the city code from range tomorrow to six months
    #returns data of the flight
    flight = flight_search.check_flights(ORIGIN_CITY_IATA,city_code,tomorrow,six_month_from_today)

    try: #try checking if theres a lower price flight if there isnt just continue
        #if price is lower fill all the data with new data in google sheets
        if flight.price < dict["price"]:
            #make the routes looks nice on excel i could use join but it was too late i need to go to sleep
            routes = f"from {str(flight.routes[0][0])} to {str(flight.routes[0][1])},  from {str(flight.routes[1][0])} to {str(flight.routes[1][1])}"
            #replace the flights data and passing all the data i want for the excel
            data_manager.replace_flight(row_id=dict["id"],
                                        airline_back=flight.airline_back,
                                        airline_go=flight.airline_go,
                                        bags_price=flight.bags_price,
                                        routes=routes,
                                        price=flight.price,
                                        destination_city=flight.destination_city,
                                        out_date=flight.out_date,
                                        return_date=flight.return_date)

            #if flight was found and replaced send a mail and sms to our customers or to my self
            users = data_manager.get_customer_emails()
            emails = [row["email"] for row in users]
            names = [row["firstName"] for row in users]
            message = f"Low price alert! Only ₪ {flight.price}to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
            if flight.stop_overs > 0:
                message += f"\n\nFlight has {flight.stop_overs}, via {flight.via_city}."
            link = f"https://www.google.co.il/flights?hl=en#flt={flight.origin_airport}.{flight.destination_airport}.{flight.out_date}*{flight.destination_airport}.{flight.origin_airport}.{flight.return_date}"

            notification_manager.send_emails(emails, message, link)
            notification_manager.send_sms(message)

    #if theres an attribute error it means that there is no price so no flight
    except AttributeError:
        continue



