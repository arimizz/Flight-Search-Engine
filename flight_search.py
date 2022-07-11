import requests
from flight_data import FlightData

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = "wpoHPFPthnu732BacX2ljgUARyQt0WF3"


class FlightSearch:
    def __init__(self):
        #empty dict which has the codes
        self.city_codes = {}

    def get_destination_codes(self,city_names):
        print("get destination codes triggered")
        #the location end points
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        #headers for the api
        headers = {"apikey": TEQUILA_API_KEY}
        #for every city in the list of city names that we pass through do the following:
        for city in city_names:
            #query that needs to be written for the api
            query = {"term": city, "location_types": "city"}
            response = requests.get(url=location_endpoint, headers=headers, params=query)
            data = response.json()
            #the location of the code in the data
            city_code = data["locations"][0]['code']
            #appending the codes to the list in city codes by the order if paris was first the PAR will be first etc...
            self.city_codes[city] = city_code
        #returning a list with the city codes
        return self.city_codes

    def check_flights(self,origin_city_code, destination_city_code, from_time, to_time):
        print(f"Check flights triggered for {destination_city_code}")
        #getting the data for the flight to every code in the excel
        headers = {"apikey": TEQUILA_API_KEY}
        #what am i searchign for
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 5,
            "nights_in_dst_to": 7,
            "flight_type": "round",
            "one_for_city": 1,
            "adults": 2,
            "selected_cabins": "M",
            "adult_hold_bag": "1,1",
            "max_stopovers": 0,
            "curr": "ILS"
        }
        #gettign the data from the API
        response = requests.get(
            url=f"{TEQUILA_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )
        #if phyton brings data it means there is a flight if phyton cant find anything print no flights were found
        try:
            data = response.json()["data"][0]

            flight_data = FlightData(
                bags_price=data["bags_price"]["1"],
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                airline_go=data["route"][0]["airline"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                airline_back=data["route"][1]["airline"],
                routes=data["routes"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
            print(f"{flight_data.destination_city}: ₪{flight_data.price}")
            # returns the flight data so we can compare
            return flight_data
        except IndexError:
            #if you get an index error which means python didnt find any flights
            print("No flights were found.")

