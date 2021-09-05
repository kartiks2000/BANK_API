from django.urls import reverse, resolve
from django.test import SimpleTestCase
from rest_framework.test import APITestCase, APIClient
from myapp.views import IFSC_query
from rest_framework import status

class ApiUrlsTests(SimpleTestCase):

    def test_ifsc_query_is_resolved(self):
        url = reverse('ifsc_query', kwargs={'ifsc':"AKJB0000007"})
        #print("resolve(url).func - ",resolve(url).func)
        self.assertEquals(resolve(url).func.view_class, IFSC_query)


class ifsc_queryAPIViewTests(APITestCase):

    ifsc_query_url = reverse('ifsc_query', kwargs={'ifsc':"AKJB0000007"})

    def test_get_ifsc_query(self):
        response = self.client.get(self.ifsc_query_url)
        self.assertEquals(response.status_code, 200)

class leaderboardAPIViewTests(APITestCase):

    leaderboard_url_no_param = reverse('leaderboard')

    def test_get_leaderboard(self):
        response = self.client.get(self.leaderboard_url_no_param)
        self.assertEquals(response.status_code, 200)


class searchhistoryAPIViewTests(APITestCase):

    searchhistory_url = reverse('searchhistory')

    def test_get_searchhistory(self):
        response = self.client.get(self.searchhistory_url)
        self.assertEquals(response.status_code, 200)


class ifsc_hitAPIViewTests(APITestCase):

    ifsc_hit_url = reverse('ifsc_hit')

    def test_get_searchhistory(self):
        response = self.client.get(self.ifsc_hit_url)
        self.assertEquals(response.status_code, 200)


class url_hitAPIViewTests(APITestCase):

    url_hit_url = reverse('url_hit')

    def test_get_searchhistory(self):
        response = self.client.get(self.url_hit_url)
        self.assertEquals(response.status_code, 200)
