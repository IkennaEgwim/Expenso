from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Expense, Category, Budget

class ExpensoAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
    
    def test_add_expense(self):
        category = Category.objects.create(user=self.user, name='Food')
        response = self.client.post(reverse('add_expense'), {
            'category': category.id,
            'amount': '50.00',
            'date': '2024-07-10',
            'notes': 'Dinner'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 1)
    
    def test_update_expense(self):
        category = Category.objects.create(user=self.user, name='Food')
        expense = Expense.objects.create(user=self.user, category=category, amount='50.00', date='2024-07-10', notes='Dinner')
        response = self.client.post(reverse('update_expense', args=[expense.id]), {
            'category': category.id,
            'amount': '60.00',
            'date': '2024-07-10',
            'notes': 'Dinner'
        })
        self.assertEqual(response.status_code, 302)
        expense.refresh_from_db()
        self.assertEqual(expense.amount, 60.00)
    
    def test_delete_expense(self):
        category = Category.objects.create(user=self.user, name='Food')
        expense = Expense.objects.create(user=self.user, category=category, amount='50.00', date='2024-07-10', notes='Dinner')
        response = self.client.post(reverse('delete_expense', args=[expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.count(), 0)