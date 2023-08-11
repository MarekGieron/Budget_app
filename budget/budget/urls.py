from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from budget_app.views import (IncomeListView, ExpenseListView, BudgetListView, SavingsListView,
                              IncomeFormView, IncomeDeleteView, HomeView, CustomLoginView, create_user_view,
                              ExpenseFormView, ExpenseCategoryAddView, ExpenseCategoryDeleteView, DeleteCategoryView,
                              DeleteExpenseView, MoveToSavingsView, CreateBudgetView, BudgetListView,
                              SetDefaultUserView, CreateSavingsView, DeleteSavingsView)


urlpatterns = [
    path('', CustomLoginView.as_view(), name='home'),
    path('create_user/', create_user_view, name='create_user'),
    path('admin/', admin.site.urls),
    path('incomes/', IncomeListView.as_view(), name='income-list'),
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('budgets/', BudgetListView.as_view(), name='budget-list'),
    path('savings/', SavingsListView.as_view(), name='savings-list'),
    path('incomes/form/', IncomeFormView.as_view(), name='income-form'),
    path('incomes/delete/<int:pk>/', IncomeDeleteView.as_view(), name='income-delete'),
    path('add-expense/', ExpenseFormView.as_view(), name='expense-form'),
    path('add-expense/', ExpenseFormView.as_view(), name='add-expense'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-expense-category/', ExpenseCategoryAddView.as_view(), name='add-expense-category'),
    path('expense-category/<int:category_id>/delete/', ExpenseCategoryDeleteView.as_view(), name='delete-expense-category'),
    path('category/<int:pk>/delete/', DeleteCategoryView.as_view(), name='category-delete'),
    path('expense/<int:pk>/delete/', DeleteExpenseView.as_view(), name='expense-delete'),
    path('move-to-savings/', MoveToSavingsView.as_view(), name='move-to-savings'),
    path('create-budget/', CreateBudgetView.as_view(), name='create-budget'),
    path('budget-list/', BudgetListView.as_view(), name='budget-list'),
    path('set-default-user/', SetDefaultUserView.as_view(), name='set-default-user'),
    path('savings/create/', CreateSavingsView.as_view(), name='create-savings'),
    path('savings/<int:pk>/delete/', DeleteSavingsView.as_view(), name='delete-savings'),
]