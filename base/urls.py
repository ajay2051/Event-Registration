from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('event/<str:pk>/', views.eventpage, name='event'),
    path('registration_confirmation/<str:pk>/', views.registration_confirmation, name='registration_confirmation'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('account/', views.account, name='account'),
    path('project_submission/<str:pk>/', views.project_submission, name='project_submission'),
    path('update_project_submission/<str:pk>/', views.update_submission, name='update_submission'),


    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),
]