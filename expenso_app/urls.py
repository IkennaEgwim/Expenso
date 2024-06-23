from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_category/', views.add_category, name='add_category'),
]