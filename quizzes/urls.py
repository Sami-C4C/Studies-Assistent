# quizzes/urls.py

from django.urls import path
from . import views
from .views import check_answers

urlpatterns = [
    path('', views.index_view, name='index'),
    path('tools.html', views.tools_view, name='tools'),
    path('guidelines.html', views.guidelines_view, name='guidelines'),
    path('tipps.html', views.tipps_view, name='tipps'),
    path('KI-Helfer.html', views.helfer_view, name='helfer'),
    path('assistent.html', views.assistent_view, name='assistent'),
    path('generated_quiz/', views.generate_quiz, name='generated_quiz'),
    path('saved_quizzes/', views.saved_quizzes, name='saved_quizzes'),
    path('view_quiz/<int:quiz_id>/', views.view_quiz, name='view_quiz'),
    path('save_quiz/', views.save_quiz, name='save_quiz'),
    path('quizzes/check_answers/<int:quiz_id>/', check_answers, name='check_answers'),

]
