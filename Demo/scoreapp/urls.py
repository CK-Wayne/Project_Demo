from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_scores, name='show_scores'),
]