from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from budget.budget_app.models import Expense
from budget.budget_app.views import ExpenseListView


class ExpenseListViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_method(self):
        response = self.client.get(reverse('expense-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expense_list.html')
        self.assertQuerysetEqual(response.context['expenses'], Expense.objects.all(), ordered=False)
