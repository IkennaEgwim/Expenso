from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
