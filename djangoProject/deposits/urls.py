from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_financial_data),
    path('deposit/', views.deposit_list),
    path('saving/', views.saving_list),
    path('bank_list/', views.bank_list),
    path('user/deposits/', views.user_deposit_list, name='user_deposit_list'),
    path('user/savings/', views.user_saving_list, name='user_saving_list'),
    path('deposit/<str:deposit_id>/toggle-like/', views.deposit_toggle_contract_user),
    path('deposit/<str:deposit_id>/contract-status/', views.deposit_get_contract_status, name='deposit_get_contract_status'),
    path('saving/<str:saving_id>/toggle-like/', views.saving_toggle_contract_user),
    path('saving/<str:saving_id>/contract-status/', views.saving_get_contract_status, name='saving_get_contract_status'),
]


