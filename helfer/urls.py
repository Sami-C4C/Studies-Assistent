# helfer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('Studies-helfer/', views.ki_helfer_view, name='studies-helfer'),
]
