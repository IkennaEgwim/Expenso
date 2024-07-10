from django import forms
from .models import Expense, Category, Budget

class DateInput(forms.DateInput):
    input_type = 'date'

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'notes']
        widgets = {
            'date': DateInput(),
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(), 'end_date': DateInput()
        }

