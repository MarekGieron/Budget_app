# test_models.py
import pytest
from datetime import date
from django.contrib.auth.models import User
from budget.budget_app.models import Income, Expense, Budget, Savings, ExpenseCategory
import os
import django
from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "budget_app.settings")
django.setup()

@pytest.fixture
def sample_user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def sample_budget(sample_user):
    return Budget.objects.create(name='Test Budget', user=sample_user)


@pytest.fixture
def sample_income(sample_budget):
    return Income.objects.create(source='Salary', amount=1000, date=date.today(), budget=sample_budget)


@pytest.fixture
def sample_expense_category():
    return ExpenseCategory.objects.create(name='Groceries')


@pytest.fixture
def sample_expense(sample_expense_category):
    return Expense.objects.create(category=sample_expense_category, description='Grocery shopping', amount=50, date=date.today())


@pytest.fixture
def sample_savings(sample_user):
    return Savings.objects.create(name='Emergency Fund', amount=500, user=sample_user)


def test_income_model(sample_income):
    assert str(sample_income) == "Salary - 1000.00 ({})".format(date.today())


def test_expense_model(sample_expense):
    assert str(sample_expense) == "Groceries - 50.00 ({})".format(date.today())


def test_budget_model(sample_budget):
    assert str(sample_budget) == "Test Budget"


def test_savings_model(sample_savings):
    assert str(sample_savings) == "Emergency Fund"


def test_update_budget_total_income(sample_income, sample_budget):
    updated_budget = Budget.objects.get(pk=sample_budget.pk)
    assert updated_budget.total_income == sample_income.amount


def test_expense_category_model(sample_expense_category):
    assert str(sample_expense_category) == "Groceries"


def test_income_related_to_budget(sample_income, sample_budget):
    assert sample_income.budget == sample_budget


def test_expense_related_to_expense_category(sample_expense, sample_expense_category):
    assert sample_expense.category == sample_expense_category


def test_savings_related_to_user(sample_savings, sample_user):
    assert sample_savings.user == sample_user
