from django.urls import path
from .views import payout_api, get_balance_api, get_payouts_api, ledger_api

urlpatterns = [
    path('v1/payouts/', payout_api),
    path('v1/balance/<int:merchant_id>/', get_balance_api),
    path('v1/payouts/<int:merchant_id>/', get_payouts_api),
    path('v1/ledger/<int:merchant_id>/', ledger_api),
]