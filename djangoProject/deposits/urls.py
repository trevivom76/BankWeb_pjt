from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_financial_data),
    path('deposit/', views.deposit_list),
    path('deposit/<int:deposit_id>/', views.deposit_detail),
    path('saving/', views.saving_list),
    path('saving/<int:saving_id>/', views.saving_detail),
]
