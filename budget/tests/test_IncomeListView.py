import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from budget.budget_app.models import Income
from budget.budget_app.views import IncomeListView


class IncomeListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_method(self):
        response = self.client.get(reverse('income-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income_list.html')

    def test_post_method(self):
        initial_income_count = Income.objects.count()
        response = self.client.post(reverse('income-list'), {
            'amount': '1000.00',
            'source': 'Salary',
            'date': datetime.date.today()
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertEqual(Income.objects.count(), initial_income_count + 1)
        self.assertEqual(response.url, reverse('income-list'))  # Redirect to income list
