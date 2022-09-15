from datetime import datetime
from typing import List


class Flight:
    def __init__(
            self,
            origin_iata: str, origin_city: str, departure_datetime: datetime, coordinates_city_origin: float,
            destination_iata: str, destination_city: str, arrival_datetime: datetime, coordinates_city_destination: float,
            countries: List[str]
    ):
        self.origin_iata = origin_iata
        self.origin_city = origin_city
        self.departure_datetime = departure_datetime
        self.coordinates_city_origin = coordinates_city_origin


        self.destination_iata = destination_iata
        self.arrival_datetime = arrival_datetime
        self.destination_city = destination_city
        self.coordinates_city_destination = coordinates_city_destination

        self.countries = countries
    def __repr__(self):
        data = [
            self.origin_iata,
            self.origin_city,
            self.departure_datetime,
            self.coordinates_city_origin,

            self.destination_iata,
            self.destination_city,
            self.arrival_datetime,
            self.coordinates_city_destination,

            self.countries
        ]
        data_repr = []

        for datum in data:
            if datum is None:
                continue

            if isinstance(datum, datetime):
                data_repr.append(f'[{datum}]')
            else:
                data_repr.append(f'{datum}')

        res = ' — '.join(data_repr)

        return res

    @staticmethod
    def get_point_iata(flight_dict, point):
        point_data = flight_dict['airport'].get(point)

        if point_data is None:
            point_iata = None
        else:
            point_iata = flight_dict['airport'][point]['code']['iata']

        return point_iata

    @staticmethod
    def get_event_datetime(flight_dict, event: str):
        event_timestamp = flight_dict['time']['real'].get(event)

        if event_timestamp is None:
            event_datetime = None
        else:
            event_datetime = datetime.fromtimestamp(event_timestamp)

        return event_datetime

    @staticmethod
    def get_point_city(flight_dict, point):
        point_city = flight_dict['airport'].get(point)

        if point_city is not None:
            point_city = point_city['position']['region']['city']

        return point_city

    @staticmethod
    def get_coordinates_city(flight_dict, point):
        point_coordinates = flight_dict['airport'].get(point)

        coordinates_city_latitude, coordinates_city_longitude = None, None

        if point_coordinates is not None:
            coordinates_city_latitude = point_coordinates['position']['latitude']
            coordinates_city_longitude = point_coordinates['position']['longitude']

        return coordinates_city_latitude, coordinates_city_longitude

    @staticmethod
    def from_dict(flight_dict):
        origin_iata = Flight.get_point_iata(flight_dict, 'origin')
        destination_iata = Flight.get_point_iata(flight_dict, 'destination')

        countries = []

        for key in ('origin', 'destination'):
            country_data = flight_dict['airport'].get(key)

            if country_data is not None:
                country = country_data['position']['country']['name']
            else:
                country = None

            countries.append(country)

        departure_datetime = \
            Flight.get_event_datetime(flight_dict, 'departure')
        arrival_datetime =\
            Flight.get_event_datetime(flight_dict, 'arrival')

        origin_city = Flight.get_point_city(flight_dict, 'origin')
        destination_city = Flight.get_point_city(flight_dict, 'destination')

        coordinates_city_origin = Flight.get_coordinates_city(flight_dict, 'origin')
        coordinates_city_destination = Flight.get_coordinates_city(flight_dict, 'destination')

        return Flight(
            origin_iata, origin_city, departure_datetime, coordinates_city_origin,
            destination_iata, destination_city, arrival_datetime,
            coordinates_city_destination, countries
        )
