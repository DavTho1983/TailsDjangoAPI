from django.test import TestCase
from Postcodes.views import PostcodesWithinRadius
from django.conf import settings


URL = settings.STORES_DATA_URL + "\within_5_miles_of_Camden.txt"


class ModelTests(TestCase):
    def test_get_postcode_data_under_20_km(self):
        """Test a postcode gets the right list of nearby postcodes"""
        postcode = "HP20 1DH"
        radius = 20
        nearby_postcodes = 'HP20 1DH'
        returned_postcodes = []

        p = PostcodesWithinRadius()
        results = p.get_postcodes_within_radius(postcode, radius)
        for result in results.values():
            returned_postcodes.append(result['postcode'])

        self.assertTrue(nearby_postcodes in returned_postcodes)
