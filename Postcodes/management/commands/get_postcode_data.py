from django.core.management import BaseCommand

from Postcodes.models import Postcode
from Postcodes.views import PostcodesWithinRadius
from django.conf import settings

import pandas as pd

URL = settings.STORES_DATA_URL + '\stores.json'

class Command(BaseCommand):


    def __init__(self):
        self.postcode = Postcode()
        self.postcodes_in_radius = PostcodesWithinRadius()
        self.stores = pd.read_json(URL)

    def execute(self, *args, **options):

        for row in self.stores.iterrows():
            print(row[1][0], row[1][1])
            postcode_data = self.postcodes_in_radius.convert_postcode_to_lat_lon(row[1][1])

            try:
                postcode = Postcode(
                    name=row[1][0].replace('_', ' '),
                    postcode=row[1][1],
                    latitude = postcode_data['result'][0]['longitude'],
                    longitude = postcode_data['result'][0]['latitude'],
                )
                postcode.save()

            except:
                postcode = Postcode(
                    name=row[1][0].replace('_', ' '),
                    postcode=row[1][1],
                )
                postcode.save()