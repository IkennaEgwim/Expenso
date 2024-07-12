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
from django.utils import timezone
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum

# Dictionary to map month names to month numbers
MONTH_CHOICES_DICT = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12,
}

# Create your views here.
def home(request):
    return render(request, 'expenso_app/home.html')

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

   # Calculate the remaining budget for each category in each month
    remaining_budgets = {}
    for budget in budgets:
        if budget.category not in remaining_budgets:
            remaining_budgets[budget.category.name] = {}

        month_expenses = expenses.filter(category=budget.category, date__month=MONTH_CHOICES_DICT[budget.month])
        total_expenses = month_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        remaining_budgets[budget.category.name][budget.month] = budget.amount - total_expenses

    context = {
        'expenses': expenses,
        'categories': categories,
        'budgets': budgets,
        'remaining_budgets': remaining_budgets,
        'welcome_message': "Welcome to Expenso!"
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
            messages.success(request, f'Expense of {expense.amount} added successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenso_app/add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, f'Expense of {expense.amount} updated successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenso_app/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, f'Expense deleted successfully!')
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
            messages.success(request, f'Category "{category.name}" added successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expenso_app/manage_categories.html', {'form': form, 'categories': categories})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'expenso_app/edit_category.html', {'form': form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f'Category deleted successfully!')
        return redirect('manage_categories')
    return render(request, 'expenso_app/delete_category.html', {'category': category})

@login_required
def manage_budgets(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            existing_budget = Budget.objects.filter(user=request.user, category=budget.category, month=budget.month).first()
            if existing_budget:
                existing_budget.amount += budget.amount
                existing_budget.save()
                messages.success(request, f"Budget for {budget.category.name} in {budget.month} updated to {existing_budget.amount}.")
            else:
                budget.save()
                messages.success(request, f"Budget for {budget.category.name} in {budget.month} added!")
            return redirect('manage_budgets')
    else:
        form = BudgetForm()
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'expenso_app/manage_budgets.html', {'form': form, 'budgets': budgets})

@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, f'Budget of {budget.amount} for {budget.month} in {budget.category.name} updated successfully!')
            return redirect('manage_budgets')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'expenso_app/edit_budget.html', {'form': form})

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, f'Budget deleted successfully!')
        return redirect('manage_budgets')
    return render(request, 'expenso_app/delete_budget.html', {'budget': budget})