from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Income(models.Model):
    """
    Model representing an income record.
    """
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='incomes', blank=True, null=True)

    def __str__(self):
        return f"{self.source} - {self.amount} ({self.date})"


class Expense(models.Model):
    """
    Model representing an expense record.
    """
    category = models.ForeignKey('ExpenseCategory', on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"

    def delete(self, *args, **kwargs):
        other_category, created = ExpenseCategory.objects.get_or_create(name="Other")
        self.category = other_category
        self.save()
        super().delete(*args, **kwargs)


class Budget(models.Model):
    """
    Model representing a budget.
    """
    name = models.CharField(max_length=100, default="Nowy Budżet")
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    savings = models.ManyToManyField('Savings', related_name='budgets', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def label_for_form(self):
        return f"Budżet {self.id}"


class Savings(models.Model):
    """
    Model representing savings goals.
    """
    name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def label_for_form(self):
        return f"Do Oszczędności {self.id}"

    def get_absolute_url(self):
        return reverse('delete-savings', args=[str(self.budget.id), str(self.id)])


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    """
    Model representing expense categories.
    """
    def __str__(self):
        return self.name


def delete(self, *args, **kwargs):
        other_category, created = ExpenseCategory.objects.get_or_create(name="Other")
        expenses_to_update = Expense.objects.filter(category=self)
        expenses_to_update.update(category=other_category)
        super().delete(*args, **kwargs)


@receiver(post_save, sender=Income)
def update_budget_total_income(sender, instance, **kwargs):
    # Update 'budget' field in the Income model
    instance.budget.total_income += instance.amount
    instance.budget.save()

    # Update 'total_income' field in the Budget model
    total_income = Income.objects.filter(budget=instance.budget).aggregate(total_income=models.Sum('amount'))['total_income'] or 0
    instance.budget.total_income = total_income
    instance.budget.save()
