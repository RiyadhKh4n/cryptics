from django.test import TestCase
from .models import Portfolio, User

from django.urls import resolve, reverse


class TestViews(TestCase):

    def setUp(self):
        User.objects.create_user(username='john', email='john@doe.com',
                                 password='123')
        self.client.login(username='john', password='123')

    def test_get_portfolio_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

    def test_create_portfolio(self):
        url = reverse('create_portfolio_url')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/create_portfolio.html')

    def test_create_portfolio_form(self):
        url = reverse('create_portfolio_url')
        john = User.objects.get(username='john')
        response = self.client.post(
            url, {"name": "ftx", "slug": "ftx", "user": john})
        count = Portfolio.objects.count()
        self.assertEqual(count, 1)
