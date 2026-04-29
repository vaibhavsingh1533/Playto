from celery import shared_task
import random
from django.db import transaction
from .models import Payout, Ledger


@shared_task
def process_payouts(payout_id):
    try:
        with transaction.atomic():
            # 🔒 lock payout row
            p = Payout.objects.select_for_update().get(id=payout_id)

            # idempotent guard
            if p.status not in ["PENDING", "PROCESSING"]:
                return

            # move to processing if first time
            if p.status == "PENDING":
                p.status = "PROCESSING"
                p.save()

            r = random.randint(1, 100)

            if r <= 70:
                # ✅ SUCCESS → convert HELD → DEBIT
                p.status = "SUCCESS"

                Ledger.objects.create(
                    merchant=p.merchant,
                    amount=p.amount,
                    type="DEBIT"
                )

            elif r <= 90:
                # ❌ FAILED → release HELD (no credit, no debit)
                p.status = "FAILED"

            else:
                # ⏳ keep processing (simulate delay/retry)
                p.retries += 1
                p.status = "PROCESSING"
                p.save()
                return

            p.save()

    except Payout.DoesNotExist:
        pass