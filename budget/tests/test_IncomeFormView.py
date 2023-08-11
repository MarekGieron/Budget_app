from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from budget.budget_app.models import Income, Budget
from budget.budget_app.forms import IncomeForm
from budget.budget_app.views import IncomeFormView

class IncomeFormViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_get_method(self):
        response = self.client.get(reverse('income-form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income_form.html')
        self.assertIsInstance(response.context['form'], IncomeForm)

    def test_valid_post_method(self):
        initial_income_count = Income.objects.count()
        initial_budget = Budget.objects.get_or_create(name='Mój Budżet')[0]
        response = self.client.post(reverse('income-form'), {
            'amount': '1000.00',
            'source': 'Salary',
            'date': '2023-08-11'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertEqual(Income.objects.count(), initial_income_count + 1)
        self.assertEqual(response.url, reverse('income-list'))  # Redirect to income list

        updated_budget = Budget.objects.get(name='Mój Budżet')
        self.assertEqual(updated_budget.total_income, initial_budget.total_income + 1000.00)

    def test_invalid_post_method(self):
        response = self.client.post(reverse('income-form'), {
            'amount': '-100.00',  # Invalid amount
            'source': 'Salary',
            'date': '2023-08-11'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income_form.html')
        self.assertContains(response, 'Amount must be greater than zero.')  # Error message should be displayed
