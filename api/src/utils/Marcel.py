import requests
from pprint import pprint
from datetime import datetime

class Marcel():
    def __init__(self):
        self.api_url = "https://api.classnco.com/api/v3/Marcel/passenger_requests?locale=fr"
        self.available_seats = {
            "Berline": {
                "id": "1",
                "seats": 4
            }, 
            "Zoe": {
                "id": "1036",
                "seats": 2
            }, 
            "Business": {
                "id": "2",
                "seats": 4
            },
            "Van": {
                "id": "3",
                "seats": 7
            },
            "moto": {
                "id": "380",
                "seats": 1
            }
        }

    def build_payload(self, from_, to):
        return {
            "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+02:00"),
            "address_pick_up": from_,
            "distance_unit": "km",
            "type": 1,
            "ride_date": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "request_type": "PassengerRequest",
            "address_drop_off": to,
            "options": [],
            "route": [],
            "vehicle_type": {},
            "channel": 2
        }

    def send_request(self, mode_id, from_, to):
        payload = self.build_payload(from_, to)
        payload["vehicle_type"]["id"] = mode_id
        response = requests.post(self.api_url, json=payload)
        if response.status_code == 201:
            return response.json()
        print("[Error] Marcel API return {} {}".format(response.status_code, response.json()))  
        return {}

    def get_estimation(self, address_pick_up, address_drop_off, nb_seats, iteration):
        estimations = {}
        from_ = {
            "lat": address_pick_up["coordinates"]["lat"],
            "long": address_pick_up["coordinates"]["long"],
            "zip_code": address_pick_up["zip_code"],
            "name": address_pick_up["address"]
        }
        to = {
            "lat": address_drop_off["coordinates"]["lat"],
            "long": address_drop_off["coordinates"]["long"],
            "zip_code": address_drop_off["zip_code"],
            "name": address_drop_off["address"]
        }
        for mode, params in self.available_seats.items():
            if params["seats"] >= nb_seats:
                estimation = self.send_request(params["id"], from_, to)
                if estimation:
                    estimations[mode] = {
                        "price": estimation['customer_price'] / 100.0,
                        "distance": estimation["distance"] / 1000.0,
                        "duration": estimation["duration"],
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "iteration": iteration
                    }
        return estimations