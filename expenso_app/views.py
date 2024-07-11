from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Expense, Category, Budget
from django.contrib.auth.models import User
from .forms import ExpenseForm, CategoryForm, BudgetForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DeleteView
from django.views import generic

# Create your views here.
def home(request):
    return render(request, 'expenso_app/home.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def dashboard(request):
    # Logic to fetch expenses, categories, etc.
    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)
    context = {
        'expenses': expenses,
        'categories': categories,
        'budgets': budgets,
        'welcome_message': "Welcome to Expenso! Track your expenses, manage your budget, and gain insights into your spending habits."
    }
    return render(request, 'expenso_app/dashboard.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, f'Expense of {expense.amount} added successfully.')
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenso_app/add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, f'Expense of {expense.amount} updated successfully.')
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenso_app/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = Expense.objects.get(id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, f'Expense deleted successfully.')
        return redirect('dashboard')
    return render(request, 'expenso_app/delete_expense.html', {'expense': expense})

@login_required
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f'Category "{category.name}" added successfully.')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenso_app/manage_categories.html', {'form': form, 'categories': categories})

@login_required
def manage_budgets(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, f'Budget of {budget.amount} for {budget.period} in {budget.category.name} added successfully.')
            return redirect('manage_budgets')
    else:
        form = BudgetForm()
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'expenso_app/manage_budgets.html', {'form': form, 'budgets': budgets})