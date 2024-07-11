from django.urls import path
from . import views
from .views import home, SignUp

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('manage-budgets/', views.manage_budgets, name='manage_budgets'),
    path('', home, name='home'),
    path('signup/', SignUp.as_view(), name='signup'),
    
]