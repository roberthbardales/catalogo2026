from django.urls import path

from . import views

app_name = 'app_inventory'

urlpatterns = [
    path('', views.MovementListView.as_view(), name='movement-list'),
    path('crear/', views.MovementCreateView.as_view(), name='movement-create'),
]
