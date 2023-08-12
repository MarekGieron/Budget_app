from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Income, Expense, Budget, Savings
from .forms import (IncomeForm, ExpenseForm, ExpenseCategoryForm, MoveToSavingsForm, CreateBudgetForm,
                    ExpenseCategoryDeleteForm, NewSavingsForm, DeleteSavingsForm, ExpenseCategory)
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse, resolve
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect


def create_user_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Tworzenie użytkownika na podstawie modelu User
        user = User.objects.create_user(username=username, password=password)
        # Możesz dodać dalszą logikę lub przekierowanie na inny widok
        return redirect('success_page')

    return render(request, 'create_user.html')


class CustomLoginView(LoginView):
    """Custom login view with redirection and initial user creation."""
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if User.objects.count() == 0:
            return redirect('create_user')  # Redirect to user creation if no users exist
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('income-list')  # Redirect after successful login


class IncomeListView(View):
    """
    View for listing and managing income entries.
    """
    template_name = 'income_list.html'

    @method_decorator(login_required)
    def get(self, request):
        income_id = request.GET.get('income_id')

        if income_id:
            try:
                income = Income.objects.get(id=income_id)
                income.delete()
            except Income.DoesNotExist:
                pass

            return redirect(reverse('income-list'))

        incomes = Income.objects.order_by('-date')
        return render(request, self.template_name, {'incomes': incomes})

    @method_decorator(login_required)
    def post(self, request):
        amount = request.POST.get('amount')
        source = request.POST.get('source')
        date = request.POST.get('date')

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")

            Income.objects.create(
                amount=amount,
                source=source,
                date=date
            )
            return redirect('income-list')
        except ValueError as e:
            error_message = str(e)

        incomes = Income.objects.all()
        return render(request, self.template_name, {'incomes': incomes, 'error_message': error_message})


class IncomeFormView(View):
    """
    View for handling the income form.
    """
    @method_decorator(login_required)
    def get(self, request):
        form = IncomeForm()
        return render(request, 'income_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            # Przypisz przychód do odpowiedniego budżetu
            budget, created = Budget.objects.get_or_create(name='Mój Budżet')
            budget.total_income += income.amount
            budget.save()
            income.budget = budget
            income.save()
            return redirect('income-list')
        return render(request, 'income_form.html', {'form': form})


class ExpenseListView(View):
    """
    View for listing expenses.
    """
    @method_decorator(login_required)
    def get(self, request):
        expenses = Expense.objects.all()
        return render(request, 'expense_list.html', {'expenses': expenses})


class BudgetListView(View):
    """
    View for listing budgets.
    """
    @method_decorator(login_required)
    def get(self, request):
        budgets = Budget.objects.all()
        return render(request, 'budget_list.html', {'budgets': budgets})


@method_decorator(login_required, name='dispatch')
class SavingsListView(View):
    """
    View for listing savings.
    """
    def get(self, request):
        savings = Savings.objects.all()
        return render(request, 'savings_list.html', {'savings': savings})


@method_decorator(login_required, name='dispatch')
class IncomeDeleteView(View):
    """
    View for deleting an income entry.
    """
    def post(self, request, pk):
        income = get_object_or_404(Income, pk=pk)

        # Pobierz budżet powiązany z przychodem
        budget = income.budget

        # Zaktualizuj budżet po usunięciu przychodu
        if budget:
            budget.total_income -= income.amount
            budget.save()

        income.delete()
        return redirect(reverse('income-list'))


class HomeView(View):
    """
    View for displaying the home page.
    """
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'home.html')


@method_decorator(login_required, name='dispatch')
class ExpenseFormView(View):
    """
    View for adding a new expense.
    """
    def get(self, request):
        """Handle GET request for rendering the expense form."""
        form = ExpenseForm()
        return render(request, 'expense_form.html', {'form': form})

    def post(self, request):
        """Handle POST request for submitting the expense form."""
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            # Assign the expense to the appropriate budget
            budget, created = Budget.objects.get_or_create(name='Mój Budżet')
            budget.total_income -= expense.amount
            budget.save()
            expense.budget = budget
            expense.save()
            return redirect('expense-list')
        return render(request, 'expense_form.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ExpenseCategoryAddView(View):

    template_name = 'add_expense_category.html'
    """
    View for adding a new expense category.
    """
    def get(self, request):
        """Handle GET request for rendering the expense category form."""
        form = ExpenseCategoryForm()
        categories = ExpenseCategory.objects.all()  # Pobierz istniejące kategorie
        return render(request, self.template_name, {'form': form, 'categories': categories})

    def post(self, request):
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense-list')  # Przekierowanie na listę wydatków
        categories = ExpenseCategory.objects.all()  # Pobierz istniejące kategorie
        return render(request, self.template_name, {'form': form, 'categories': categories})


@method_decorator(login_required, name='dispatch')
class ExpenseCategoryDeleteView(View):
    """
    View for deleting an expense category.
    """
    template_name = 'delete_expense_category.html'

    def get(self, request, category_id):
        """Handle GET request for rendering the confirmation page for deleting an expense category."""
        category = ExpenseCategory.objects.get(id=category_id)
        return render(request, self.template_name, {'category': category})

    def post(self, request, category_id):
        """Handle POST request for deleting an expense category."""
        category = ExpenseCategory.objects.get(id=category_id)
        if request.method == 'POST':
            category.delete()
            return redirect('expense-list')  # Przekierowanie gdziekolwiek chcesz
        return render(request, self.template_name, {'category': category})


@method_decorator(login_required, name='dispatch')
class DeleteCategoryView(View):
    """
    View for confirming the deletion of an expense category.
    """
    model = ExpenseCategory
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('name-of-list-view')


@method_decorator(login_required, name='dispatch')
class DeleteExpenseView(DeleteView):
    """
    View for confirming the deletion of an expense.
    """
    model = Expense
    template_name = 'expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')  # Przekierowanie na listę wydatków


@method_decorator(login_required, name='dispatch')
class MoveToSavingsView(View):
    """
    View for moving funds from a budget to savings.
    """
    template_name = 'move_to_savings.html'

    def get(self, request, *args, **kwargs):
        form = MoveToSavingsForm(user=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = MoveToSavingsForm(request.POST, user=request.user)

        if form.is_valid():
            amount_to_move = form.cleaned_data['amount']
            from_budget_id = form.cleaned_data['from_budget']  # This will be the budget ID
            to_savings_id = form.cleaned_data['to_savings']

            try:
                from_budget = get_object_or_404(Budget, id=from_budget_id)
                to_savings = get_object_or_404(Savings, id=to_savings_id)

                if 0 < amount_to_move <= from_budget.total_income:
                    from_budget.total_income -= amount_to_move
                    to_savings.amount += amount_to_move
                    from_budget.save()
                    to_savings.save()
                    return redirect('expense-list')
                else:
                    form.add_error('amount', "Kwota przekracza dostępne środki w budżecie")
            except Budget.DoesNotExist:
                form.add_error('from_budget', "Nieprawidłowe ID budżetu")
            except Savings.DoesNotExist:
                form.add_error('to_savings', "Nieprawidłowe ID oszczędności")

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class CreateBudgetView(View):
    """
    View for creating a new budget.
    """
    template_name = 'create_budget.html'

    def post(self, request, *args, **kwargs):
        form = CreateBudgetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            total_income = form.cleaned_data['total_income']
            user = request.user
            budget = Budget.objects.create(user=user, name=name, total_income=total_income)
            return redirect('budget-list')

        return render(request, self.template_name, {'form': form})

    def get(self, request, *args, **kwargs):
        form = CreateBudgetForm()
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class BudgetListView(View):
    """
    View for displaying the list of budgets.
    """
    template_name = 'budget_list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        budgets = Budget.objects.filter(user=user)
        return render(request, self.template_name, {'budgets': budgets})


@method_decorator(login_required, name='dispatch')
class SetDefaultUserView(View):
    """
    View for setting the default user for budgets.
    """
    template_name = 'default_user_set.html'

    def get(self, request, *args, **kwargs):
        default_user = request.user
        Budget.objects.update(user=default_user)
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class CreateSavingsView(View):
    """
    View for creating a new savings entry.
    """
    template_name = 'create_savings.html'

    def get(self, request, *args, **kwargs):
        form = NewSavingsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = NewSavingsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            new_savings = Savings.objects.create(user=request.user, name=name, amount=0)
            return redirect('savings-list', pk=new_savings.pk)
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class DeleteSavingsView(View):
    """
    View for deleting a savings entry.
    """
    def post(self, request, *args, **kwargs):
        form = DeleteSavingsForm(request.POST)

        if form.is_valid():
            # Pobierz aktualny URL, aby zidentyfikować parametry 'budget_id' i 'savings_id'
            current_url = resolve(request.path_info)
            budget_id = current_url.kwargs.get('budget_id')
            savings_id = current_url.kwargs.get('savings_id')

            if budget_id is not None and savings_id is not None:
                budget = get_object_or_404(Budget, id=budget_id)
                savings = budget.savings.filter(id=savings_id).first()

                if savings:
                    # Odejmujemy oszczędności od kwoty budżetu
                    budget.total_income -= savings.amount
                    budget.save()

                    # Usuwamy oszczędności z relacji i z bazy danych
                    budget.savings.remove(savings)
                    savings.delete()

        return HttpResponseRedirect(reverse('savings-list'))  # Przekierowanie po wykonaniu operacji