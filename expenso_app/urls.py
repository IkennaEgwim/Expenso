from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_category/', views.add_category, name='add_category'),
    path('set_budget/', views.set_budget, name='set_budget'),
    path('accounts/login/', views.login_view),
    path('update_expense/<int:pk>/', views.update_expense, name='update_expense'),
    path('update_category/<int:pk>/', views.update_category, name='update_category'),
    path('update_budget/<int:pk>/', views.update_budget, name='update_budget'),
    path('delete_expense/<int:pk>/', views.ExpenseDeleteView.as_view(), name='delete_expense'),
    path('delete_category/<int:pk>/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('delete_budget/<int:pk>/', views.BudgetDeleteView.as_view(), name='delete_budget'),
]