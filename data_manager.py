import requests


SHEETY_ENDPOINT_SHEET = "https://api.sheety.co/e1651d8e666699299dfd3fbca3f282f4/prices/price"
SHEET_USERS_ENDPOINT = "https://api.sheety.co/e1651d8e666699299dfd3fbca3f282f4/prices/users"

class DataManager:

    def __init__(self):
        #contain the get request with all the data in a dict
        self.destination_data = {}

    def get_destination_data(self):
        #gets all the requests data and put it in the empty dict
        response = requests.get(url=SHEETY_ENDPOINT_SHEET)
        data = response.json()
        #all the data we need is in the "price" key which is the name of the sheet
        self.destination_data = data["price"]
        return self.destination_data

    def update_destination_codes(self,city_codes):
        #for evrey city in the google sheet
        for city_data in self.destination_data:
            #if the name of the city is in the dict city codes
            #then make the city code and code of the city and put it in the google sheet
            city_name = city_data["city"]
            if city_data["city"] in city_codes:
                print(f"Brining the code of,{city_name}")
                new_data = {
                    "price": {
                        "iataCode": city_codes[city_name]
                    }
                }

                #update the google sheet with codes
                response = requests.put(
                    url=f"{SHEETY_ENDPOINT_SHEET}/{city_data['id']}",
                    json=new_data
                    )
                print(response.text)
                print("code has been updated")

    def replace_flight(self,row_id,airline_back,airline_go,bags_price,routes,price,destination_city,out_date,return_date):
        print(f"Brining the code of,{destination_city}")
        new_data = {
            "price": {
                "airLineBack":airline_back,
                "airLineGo":airline_go,
                "bagPrice":bags_price,
                "routes":routes,
                "lowestPrice":price,
                "departureDate":out_date,
                "returnDate":return_date


            }
        }
        # update the google sheet with codes
        response = requests.put(
            url=f"{SHEETY_ENDPOINT_SHEET}/{row_id}",
            json=new_data
        )
        print(response.text)
        print("Flight has been updated.")

    def get_customer_emails(self):
        customers_endpoint = SHEET_USERS_ENDPOINT
        response = requests.get(customers_endpoint)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data