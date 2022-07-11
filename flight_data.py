TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
TEQUILA_API_KEY = "wpoHPFPthnu732BacX2ljgUARyQt0WF3"


class FlightData:
    def __init__(self, bags_price,price, origin_city, origin_airport, destination_city, destination_airport, out_date, return_date, airline_go, airline_back, routes, passengers=2, stop_overs=0, via_city="", ):
        self.bags_price = bags_price
        self.price = price
        self.origin_city = origin_city
        self.origin_airport = origin_airport
        self.destination_city = destination_city
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.airline_go = airline_go
        self.airline_back = airline_back
        self.routes = routes
        self.passengers = passengers
        self.stop_overs = stop_overs
        self.via_city = via_city