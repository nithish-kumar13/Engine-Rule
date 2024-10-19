from django.urls import path
from .views import evaluate_rule

urlpatterns = [
    path('evaluate_rule/', evaluate_rule, name='evaluate_rule'),
]
