from django.db import transaction
from django.db.models import Sum
from .models import Ledger, Payout


def get_balance(merchant):
    credit = Ledger.objects.filter(
        merchant=merchant, type="CREDIT"
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    debit = Ledger.objects.filter(
        merchant=merchant, type="DEBIT"
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    held = Ledger.objects.filter(
        merchant=merchant, type="HELD"
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    return credit - debit - held   # ✅ FIX


@transaction.atomic
def create_payout(merchant, amount, key, bank_account_id):
    # 🔒 LOCK ledger rows (prevents race conditions)
    Ledger.objects.select_for_update().filter(merchant=merchant)

    available_balance = get_balance(merchant)

    if available_balance < amount:
        raise Exception("Insufficient balance")

    # ✅ Create payout
    payout = Payout.objects.create(
        merchant=merchant,
        amount=amount,
        bank_account_id=bank_account_id,
        status="PENDING",
        idempotency_key=key
    )

    # 🔥 HOLD funds (NOT debit yet)
    Ledger.objects.create(
        merchant=merchant,
        amount=amount,
        type="HELD"
    )

    return payout