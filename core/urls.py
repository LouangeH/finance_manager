from django.urls import path
from core.views import compte

urlpatterns = [
    path('', compte.dashboard, name='compte'),

]