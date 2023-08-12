from django import forms
from .models import Income, Expense, ExpenseCategory, Budget, Savings
from django.shortcuts import render


class IncomeForm(forms.ModelForm):
    """
    Form for creating or updating an Income object.
    """
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date']


class ExpenseForm(forms.ModelForm):
    """
    Form for creating or updating an Expense object.
    """
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date']


class ExpenseCategoryForm(forms.ModelForm):
    """
    Form for creating or updating an ExpenseCategory object.
    """
    class Meta:
        model = ExpenseCategory
        fields = ['name']


class ExpenseCategoryDeleteForm(forms.Form):
    """
    A form for deleting an expense category.
    """
    category_to_delete = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all())


class MoveToSavingsForm(forms.Form):
    """
    A form for moving funds from a budget to savings.
    """
    amount = forms.DecimalField(label='Kwota do przeniesienia', decimal_places=2, min_value=0.01)
    from_budget = forms.ChoiceField(choices=[], label='Z budżetu')
    to_savings = forms.ChoiceField(choices=[], label='Do oszczędności')

    def __init__(self, *args, user=None, **kwargs):
        """
        Initialize form with choices for budgets and savings.
        """
        super().__init__(*args, **kwargs)
        if user:
            budget_choices = [(budget.id, budget.name) for budget in Budget.objects.filter(user=user)]
            savings_choices = [(savings.id, savings.name) for savings in Savings.objects.filter(user=user)]
            self.fields['from_budget'].choices = budget_choices
            self.fields['to_savings'].choices = savings_choices


class CreateBudgetForm(forms.Form):
    """
    A form for creating a new budget.
    """
    name = forms.CharField(max_length=100)
    total_income = forms.DecimalField(max_digits=10, decimal_places=2, initial=0, required=False)


class NewSavingsForm(forms.Form):
    """
    A form for creating a new savings category.
    """
    name = forms.CharField(max_length=100, label='Savings Name')


class DeleteSavingsForm(forms.Form):
    """
    A form for confirming the deletion of a savings category.
    """
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I confirm that I want to delete this savings'
    )