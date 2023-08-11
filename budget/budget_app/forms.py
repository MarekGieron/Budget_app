from django import forms
from .models import Income, Expense, ExpenseCategory, Budget, Savings
from django.shortcuts import render


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'source', 'date']


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'description', 'amount', 'date']


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']


class ExpenseCategoryDeleteForm(forms.Form):
    category_to_delete = forms.ModelChoiceField(queryset=ExpenseCategory.objects.all())


class MoveToSavingsForm(forms.Form):
    amount = forms.DecimalField(label='Kwota do przeniesienia', decimal_places=2, min_value=0.01)
    from_budget = forms.ChoiceField(choices=[], label='Z budżetu')
    to_savings = forms.ChoiceField(choices=[], label='Do oszczędności')

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            budget_choices = [(budget.id, budget.name) for budget in Budget.objects.filter(user=user)]
            savings_choices = [(savings.id, savings.name) for savings in Savings.objects.filter(user=user)]
            self.fields['from_budget'].choices = budget_choices
            self.fields['to_savings'].choices = savings_choices


class CreateBudgetForm(forms.Form):
    name = forms.CharField(max_length=100)
    total_income = forms.DecimalField(max_digits=10, decimal_places=2, initial=0, required=False)


class NewSavingsForm(forms.Form):
    name = forms.CharField(max_length=100, label='Savings Name')


class DeleteSavingsForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I confirm that I want to delete this savings'
    )