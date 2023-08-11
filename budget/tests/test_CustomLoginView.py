import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from budget.budget_app.views import (IncomeListView, ExpenseListView, BudgetListView, SavingsListView,
                              IncomeFormView, IncomeDeleteView, HomeView, CustomLoginView, create_user_view,
                              ExpenseFormView, ExpenseCategoryAddView, ExpenseCategoryDeleteView, DeleteCategoryView,
                              DeleteExpenseView, MoveToSavingsView, CreateBudgetView, BudgetListView,
                              SetDefaultUserView, CreateSavingsView, DeleteSavingsView)

@pytest.mark.django_db
def test_custom_login_view_redirect_to_create_user():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('create_user')


@pytest.mark.django_db
def test_custom_login_view_redirect_to_income_list():
    # Stworzenie użytkownika, aby przetestować udane logowanie
    User.objects.create_user(username='testuser', password='testpass')

    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('income-list')
