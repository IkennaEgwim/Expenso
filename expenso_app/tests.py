from django.test import TestCase
from .models import Expense, Category

# Create your tests here.
class ExpenseModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Groceries")
        self.expense = Expense.objects.create(amount=50.00, date="2024-06-17", notes="Test note", category=self.category)

    def test_expense_creation(self):
        self.assertEqual(self.expense.amount, 50.00)
        self.assertEqual(self.expense.notes, "Test note")
        self.assertEqual(self.expense.category.name, "Groceries")

from django.urls import reverse
from django.test import TestCase, Client
from .models import Expense, Category

class ExpenseViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Groceries")
        self.expense = Expense.objects.create(amount=50.00, date="2024-06-17", notes="Test note", category=self.category)

    def test_expense_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Groceries")

from django.test import TestCase
from .forms import ExpenseForm
from .models import Category

class ExpenseFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Groceries")

    def test_valid_form(self):
        data = {'amount': 50.00, 'date': '2024-06-17', 'notes': 'Test note', 'category': self.category.id}
        form = ExpenseForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {'amount': '', 'date': '2024-06-17', 'notes': 'Test note', 'category': self.category.id}
        form = ExpenseForm(data=data)
        self.assertFalse(form.is_valid())


        