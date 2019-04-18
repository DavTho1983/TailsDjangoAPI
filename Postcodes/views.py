import requests
import math
from django.db.models import Q
from django.views.generic import TemplateView


from rest_framework import generics

from Postcodes.models import Postcode
from Postcodes.serializers import PostcodeSerializer

from Postcodes.constants import (
    RANDOM_POSTCODE_URL,
    POSTCODE_URL,
    ONE_DEGREE_LATITUDE_KM,
)


def get_distance_between_two_points_lat_lon(radius_km, latitude):

    radius_lat = radius_km / ONE_DEGREE_LATITUDE_KM
    one_degree_longitude_km = math.cos(latitude) * ONE_DEGREE_LATITUDE_KM
    radius_lon = radius_km / one_degree_longitude_km

    radius = {"latitude": radius_lat, "longitude": radius_lon}

    return radius


def get_random_postcode():

    querystring = {"limit": 10, "radius": 2000}

    res = requests.get(RANDOM_POSTCODE_URL, headers=None, params=querystring).json()
    return res


class IndexView(TemplateView):
    template_name = "index.html"

    model = Postcode

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Postcodes"] = Postcode.objects.order_by("name")
        return context


class PostcodessAPIListView(generics.ListAPIView):
    queryset = Postcode.objects.all()
    serializer_class = PostcodeSerializer


class PostcodesAPIID(generics.RetrieveAPIView):
    queryset = Postcode.objects.all()
    serializer_class = PostcodeSerializer


class PostcodesWithinRadius(generics.ListAPIView):
    serializer_class = PostcodeSerializer

    def get_queryset(self):
        postcode = self.kwargs.get("postcode", None)
        radius_km = self.kwargs.get("radius_km", None)
        return self.get_postcodes_within_radius(postcode, radius_km)

    def convert_postcode_to_lat_lon(self, postcode):

        GET_LAT_LON_URL = f"{POSTCODE_URL}?"

        postcode_query = {"query": postcode}

        postcode_data = requests.get(
            GET_LAT_LON_URL, headers=None, params=postcode_query
        ).json()
        return postcode_data

    def get_postcode_data_under_20_km(self, radius, postcode_data):

        postcodes_within_radius = []

        querystring = {
            "longitude": postcode_data["result"][0]["longitude"],
            "latitude": postcode_data["result"][0]["latitude"],
            "wideSearch": radius,
            "limit": 100,
        }

        res = requests.get(POSTCODE_URL, headers=None, params=querystring).json()
        for postcode in res["result"]:
            postcodes_within_radius.append(postcode["postcode"])
        return Postcode.objects.filter(postcode__in=postcodes_within_radius).order_by(
            "latitude"
        )

    def get_postcode_data_over_20_km(self, radius_km, postcode_data):

        distance = get_distance_between_two_points_lat_lon(
            radius_km, postcode_data["result"][0]["latitude"]
        )
        longitude_max = (
            postcode_data["result"][0]["longitude"] + distance["longitude"] + 180
        ) % 360 - 180
        longitude_min = (
            postcode_data["result"][0]["longitude"] - distance["longitude"] + 180
        ) % 360 - 180
        latitude_max = postcode_data["result"][0]["latitude"] + distance["latitude"]
        latitude_min = postcode_data["result"][0]["latitude"] - distance["latitude"]

        return Postcode.objects.filter(
            Q(latitude__range=(latitude_min, latitude_max))
            & Q(longitude__range=(longitude_min, longitude_max))
        ).order_by("latitude")

    def get_postcodes_within_radius(self, postcode, radius_km):

        postcode_data = self.convert_postcode_to_lat_lon(postcode)

        if radius_km <= 20:
            radius = radius_km * 1000
            return self.get_postcode_data_under_20_km(radius, postcode_data)
        else:
            return self.get_postcode_data_over_20_km(radius_km, postcode_data)
