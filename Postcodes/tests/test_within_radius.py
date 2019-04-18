from django.test import TestCase
from Postcodes.models import Postcode
from Postcodes.views import PostcodesWithinRadius
from django.conf import settings

import pandas as pd

URL = settings.STORES_DATA_URL + "\within_5_miles_of_Camden.txt"


class ModelTests(TestCase):
    def test_get_postcode_data_under_20_km(self):
        """Test a postcode gets the right list of nearby postcodes"""
        postcode = "N79RF"
        radius = 10  # 10km radius
        nearby_postcodes = pd.read_csv()

        p = PostcodesWithinRadius()
        postcode_data = p.convert_postcode_to_lat_lon
        result = p.get_postcode_data_under_20_km(5, postcode_data)

        self.assertContains(result, nearby_postcodes)
