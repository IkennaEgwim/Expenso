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
            messages.info(request, "You just logged in")
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
    # welcome_message = "Welcome to Expenso! Track your expenses, manage your budget, and gain insights into your spending habits."
    # return render(request, 'expenso_app/home.html', {'welcome_message': welcome_message})
    expenses = Expense.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)
    context = {
        'expenses': expenses,
        'categories': categories,
        'budgets': budgets,
        'welcome_message': "Welcome to Expenso! Track your expenses, manage your budget, and gain insights into your spending habits."
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
            messages.success(request, "Expense added successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error adding the expense.")     
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
            messages.success(request, "Category added successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error adding the category.")  
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
            messages.success(request, "Budget set successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error adding the budget.") 
    else:
        form = BudgetForm()
    return render(request, 'expenso_app/set_budget.html', {'form': form})

# Update Views
@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenso_app/update_expense.html', {'form': form})

@login_required
def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('home')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'expenso_app/update_category.html', {'form': form})

@login_required
def update_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully!")
            return redirect('home')
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'expenso_app/update_budget.html', {'form': form})

# Delete Views using Django's DeleteView
class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('home')
    template_name = 'expenso_app/confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('home')
    template_name = 'expenso_app/confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class BudgetDeleteView(DeleteView):
    model = Budget
    success_url = reverse_lazy('home')
    template_name = 'expenso_app/confirm_delete.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)