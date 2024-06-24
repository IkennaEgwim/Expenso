from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Expense, Category, Budget
from django.contrib.auth.models import User
from .forms import ExpenseForm, CategoryForm, BudgetForm


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'expenso_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'expenso_app/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'expenso_app/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    # Logic to fetch expenses, categories, etc.
    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)
    context = {
        'expenses': expenses,
        'categories': categories,
        'budgets': budgets,
    }
    return render(request, 'expenso_app/home.html', context)

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'expenso_app/add_expense.html', {'form': form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('home')
    else:
        form = CategoryForm()
    return render(request, 'expenso_app/add_category.html', {'form': form})

@login_required
def set_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('home')
    else:
        form = BudgetForm()
    return render(request, 'expenso_app/set_budget.html', {'form': form})

