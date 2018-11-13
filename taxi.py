from flask import Flask
from flask_restful import Api, Resource, reqparse
import math

app = Flask(__name__)
api = Api(app)

taxis = [
    {
        "name": "taxi_1",
        "location": (100, 100),
        "available": True
    },
    {
        "name": "taxi_2",
        "location": (60, 60),
        "available": True
    },
    {
        "name": "taxi_3",
        "location": (80, 80),
        "available": True
    }
]


class Taxi(Resource):

    def get(self):
        # Method to handle requests for taxi availability check
        parser = reqparse.RequestParser()
        parser.add_argument("latitude")
        parser.add_argument("longitude")
        args = parser.parse_args()

        # validates whether required fields are present in the request
        if 'latitude' not in args or 'longitude' not in args:
            return "'latitude' and 'longitude' are required", 400

        # get available taxis
        available_taxis = []
        for taxi in taxis:
            if taxi['available'] is True:
                available_taxis.append(taxi)

        # handles no taxis available scenario
        if not available_taxis:
            return "No Taxis are Available at the time", 404

        # get the closest taxi information
        distances = []
        for taxi in available_taxis:
            taxi_location = taxi['location']  # (latitude, longitude) of taxi
            customer_location = (int(args["latitude"]), int(args["longitude"]))
            distance = calculate_distance(taxi_location, customer_location)
            distances.append(distance)
        index_of_closest_taxi = distances.index(min(distances))
        closest_taxi = available_taxis[index_of_closest_taxi]

        # update taxi availability in taxis' list
        index_of_taxi_in_taxis_list = taxis.index(closest_taxi)
        taxis[index_of_taxi_in_taxis_list]['available'] = False

        return closest_taxi['name'] + " is the nearest, and will reach you shortly!"

    def patch(self):
        # Method to update taxi location and availability, once the ride is finished
        parser = reqparse.RequestParser()
        parser.add_argument("taxi_name")
        parser.add_argument("latitude")
        parser.add_argument("longitude")
        args = parser.parse_args()

        # validates whether required fields are present in the request
        if 'latitude' not in args or 'longitude' not in args or 'taxi_name' not in args:
            return "'taxi_name', 'latitude' and 'longitude' are required", 400

        # get the taxi corresponding to the given name
        taxi_to_update = None
        for taxi in taxis:
            if taxi['name'] == args['taxi_name']:
                taxi_to_update = taxi
                break
        if taxi_to_update is None:
            return "Incorrect taxi name", 400

        # update availability and location of the taxi
        index_of_taxi_in_taxis_list = taxis.index(taxi_to_update)
        taxis[index_of_taxi_in_taxis_list]['latitude'] = args['latitude']
        taxis[index_of_taxi_in_taxis_list]['longitude'] = args['longitude']
        taxis[index_of_taxi_in_taxis_list]['available'] = True
        return "Successfully updated taxi location", 200


def calculate_distance(taxi_location, customer_location):
    taxi_latitude = taxi_location[0]
    taxi_longitude = taxi_location[1]
    customer_latitude = customer_location[0]
    customer_longitude = customer_location[1]
    distance = math.sqrt((taxi_latitude-customer_latitude)**2)+((taxi_longitude-customer_longitude)**2)
    return distance


api.add_resource(Taxi, "/car")
app.run(debug=True)
