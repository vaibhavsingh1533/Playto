from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt

from .models import Merchant, Idempotency, Ledger, Payout
from .services import create_payout
from payout.tasks import process_payouts


@api_view(['POST'])
@transaction.atomic
def payout_api(request):
    merchant_id = request.data.get('merchant_id')
    amount = request.data.get('amount_paise')   # ✅ FIX
    bank_account_id = request.data.get('bank_account_id')   # ✅ NEW
    key = request.headers.get("Idempotency-Key")

    # 🔒 Validations
    if not merchant_id or not amount or not bank_account_id:
        return Response(
            {"error": "merchant_id, amount_paise and bank_account_id required"},
            status=400
        )

    try:
        amount = int(amount)
    except:
        return Response({"error": "amount_paise must be integer"}, status=400)

    if not key:
        return Response({"error": "Idempotency-Key required"}, status=400)

    merchant = get_object_or_404(Merchant, id=merchant_id)

    # ✅ Idempotency
    existing = Idempotency.objects.filter(
        key=key, merchant=merchant
    ).first()

    if existing:
        return Response(existing.response)

    try:
        payout = create_payout(merchant, amount, key, bank_account_id)  # ✅ UPDATED

        transaction.on_commit(lambda: process_payouts.delay(payout.id))

        response = {
            "payout_id": payout.id,
            "status": payout.status
        }

        Idempotency.objects.create(
            key=key,
            merchant=merchant,
            response=response
        )

        return Response(response)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(['GET'])
def get_balance_api(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)

    credit = Ledger.objects.filter(
        merchant=merchant, type="CREDIT"
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    debit = Ledger.objects.filter(
        merchant=merchant, type="DEBIT"
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    held = Ledger.objects.filter(
        merchant=merchant, type="HELD"
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return Response({
        "merchant_id": merchant.id,
        "available_balance": credit - debit - held,   # ✅ FIX
        "held_balance": held                          # ✅ NEW
    })



@api_view(['GET'])
def get_payouts_api(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)

    payouts = Payout.objects.filter(merchant=merchant).order_by('-created_at')

    data = [
        {
            "id": p.id,
            "amount": p.amount,
            "status": p.status,
            "retries": p.retries,
            "bank_account_id": p.bank_account_id,   # ✅ ADD
            "created_at": p.created_at
        }
        for p in payouts
    ]
    return Response(data)

@api_view(['GET'])
def ledger_api(request, merchant_id):
    merchant = get_object_or_404(Merchant, id=merchant_id)

    entries = Ledger.objects.filter(merchant=merchant).order_by('-created_at')

    data = [
        {
            "amount": e.amount,
            "type": e.type,
            "created_at": e.created_at
        }
        for e in entries
    ]

    return Response(data)