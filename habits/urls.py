from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('habits/', views.habit_list, name='habit_list'),
    path('habit/new/', views.habit_create, name='habit_create'),
    path('habit/<int:pk>/', views.habit_detail, name='habit_detail'),
    path('habit/<int:pk>/edit/', views.habit_update, name='habit_update'),
    path('habit/<int:pk>/delete/', views.habit_delete, name='habit_delete'),
    path('habit/<int:pk>/archive/', views.habit_archive, name='habit_archive'),
    path('habit/<int:habit_id>/toggle/<str:date>/', views.toggle_habit_record, name='toggle_habit_record'),
    path('toggle/', views.toggle_habit, name='toggle_habit'),
    path('counters/', views.get_counters, name='get_counters'),
    path('habits/archived/', views.archived_habits, name='archived_habits'),
    path('habit/<int:pk>/restore/', views.habit_restore, name='habit_restore'),

]

