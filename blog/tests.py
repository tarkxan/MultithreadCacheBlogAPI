
from django.test import TestCase, Client
from .views import ping, posts
from django.urls import reverse
import requests, json

# Create your tests here.

"""------------------------- Test Views -------------------------"""
class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.ping_url = reverse('ping')

        self.tech_tag = 'tech'
        self.history_tag = 'history'
        self.sortBy_likes = 'likes'

        self.one_post_url = reverse('posts', args=['tags={}'.format(self.tech_tag)])
        self.two_posts_url = reverse('posts', args=['tags={},{}'.format(self.tech_tag, self.history_tag)])

        self.one_post_with_default_sort_by = reverse('posts', args=['tags={}'.format(self.tech_tag),
                                                                     'sortBy={}'.format(self.sortBy_likes)])

        self.one_post_with_default_sort_by_asc = reverse('posts', args=['tags={}'.format(self.tech_tag),
                                                                    'sortBy={}'.format(self.sortBy_likes),
                                                                    'direction={}'.format('asc')])

        self.one_post_with_default_sort_by_desc = reverse('posts',
                                                          args=['tags={}'.format(self.tech_tag),
                                                                'sortBy={}'.format(self.sortBy_likes),
                                                                'direction={}'.format('desc')])
        self.api_data = None

    # get data from Hatchway API
    def get_api_data(self,
                     tag = 'tech'):

        base_url = 'https://hatchways.io/api/assessment/blog/posts?tag='
        url = base_url + tag
        api_response = requests.get(url)
        self.api_data = api_response.json()


    def test_ping_view(self):

        response = self.client.get(self.ping_url)
        self.assertEqual(response.status_code,
                         200)


    # user inserted only one tag
    def test_one_post_view(self):

        # get data from view
        response = self.client.get(self.one_post_url)
        self.assertEqual(response.status_code,
                         200)

        # get data from api
        self.get_api_data(self.tech_tag)

        # convert from bytes to dictionary
        view_data = json.loads(response.content.decode('utf-8'))

        # compare view data with api data
        self.assertEqual(self.api_data,
                         view_data['Body'])


    # user inserted two tags
    def test_two_posts_view(self):

        # get data from view
        response = self.client.get(self.two_posts_url)
        self.assertEqual(response.status_code,
                         200)

        # convert from bytes to dictionary
        view_data = json.loads(response.content.decode('utf-8'))

        view_post_set = set()
        for post in view_data['Body']['posts']:
            view_post_set.add(post['id'])

        # get data from api for tag tech
        self.get_api_data('{}'.format(self.tech_tag))
        tech_api_data = self.api_data

        # get data from api for tag history
        self.get_api_data('{}'.format(self.history_tag))
        hist_api_data = self.api_data

        api_post_set = set()
        for post in tech_api_data['posts'] + hist_api_data['posts']:
            api_post_set.add(post['id'])

        # self.assertEqual.__self__.maxDiff = None
        self.assertEqual(view_post_set,
                         api_post_set)

    def check_view_data_sorted(self,
                               view_data,
                               sortOrder = 'asc'):

        for i, post in enumerate(view_data['Body']['posts'][:-1]):

            if sortOrder == 'asc':

                # if likes[i] > likes[i+1] - then not sorted in asc order
                if post['likes'] > view_data['Body']['posts'][i+1]['likes']:
                    return False

            elif sortOrder == 'desc':

                # if likes[i] < likes[i+1] - then not sorted in desc order
                if post['likes'] < view_data['Body']['posts'][i + 1]['likes']:
                    return False


        return True

    # user inserted only one tag with sortBy=likes, default = asc
    def test_one_post_view_with_sortBy_default(self):

        # get data from view
        response = self.client.get(self.one_post_with_default_sort_by)
        self.assertEqual(response.status_code,
                         200)

        # convert from bytes to dictionary
        view_data = json.loads(response.content.decode('utf-8'))

        self.assertTrue(self.check_view_data_sorted(view_data),
                        True)

    # user inserted only one tag with sortBy=likes, direction = asc
    def test_one_post_view_with_sortBy_asc(self):
        # get data from view
        response = self.client.get(self.one_post_with_default_sort_by_asc)
        self.assertEqual(response.status_code,
                         200)

        # convert from bytes to dictionary
        view_data = json.loads(response.content.decode('utf-8'))

        self.assertTrue(self.check_view_data_sorted(view_data,
                                                    'asc'),
                        True)

    # user inserted only one tag with sortBy=likes, direction = desc
    def test_one_post_view_with_sortBy_desc(self):
        # get data from view
        response = self.client.get(self.one_post_with_default_sort_by_desc)
        self.assertEqual(response.status_code,
                         200)

        # convert from bytes to dictionary
        view_data = json.loads(response.content.decode('utf-8'))

        self.assertTrue(self.check_view_data_sorted(view_data,
                                                    'desc'),
                        True)


