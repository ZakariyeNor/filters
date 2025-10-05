from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.urls import reverse


class QueryCountTests(TestCase):
    fixtures = ["sample_products.json"]

    def test_product_list_query_budget(self):
        url = reverse("clear_dynamic_list")  # URL name of your filtered product list
        with CaptureQueriesContext(connection) as ctx:
            self.client.get(url)  # make a GET request to the view
        print("Query count:", len(ctx.captured_queries))
        self.assertLessEqual(len(ctx.captured_queries), 6)
