from django.urls import path
from . import views

urlpatterns = [
    path('', views.language_selection, name='language_selection'),
    path('calculator/', views.calculator, name='calculator'),
    path('history/', views.calculation_history, name='calculation_history'),
    path('set-language/', views.set_language, name='set_language'),
]