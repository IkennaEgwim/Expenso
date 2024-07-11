from django.urls import path
from . import views
from .views import home, SignUp

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('edit-expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),  # Added edit_category
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),  # Added delete_category
    path('manage-budgets/', views.manage_budgets, name='manage_budgets'),
    path('edit-budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),  # Added edit_budget
    path('delete-budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),  # Added delete_budget
    path('signup/', SignUp.as_view(), name='signup'),
]
