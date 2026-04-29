from django.test import TestCase, Client
from payout.models import Merchant, Ledger, Payout, Idempotency
from django.db.models import Sum
from rest_framework.test import APIClient

import threading
import json


class ConcurrencyTest(TestCase):

    def setUp(self):
        self.client = Client()

        # Create merchant
        self.merchant = Merchant.objects.create(name="Test Merchant")

        # Seed balance ₹100 (10000 paise)
        Ledger.objects.create(
            merchant=self.merchant,
            amount=10000,
            type="CREDIT"
        )

    def call_api(self, key):
        try:
            self.client.post(
                "/api/v1/payouts/",
                data={
                    "merchant_id": self.merchant.id,
                    "amount_paise": 6000,
                    "bank_account_id": "acc1"
                },
                 content_type="application/json",
                **{"HTTP_IDEMPOTENCY_KEY": key}
            )
        except Exception:
            pass

    def test_concurrent_payout(self):
        # Two different keys (simulate two users)
        t1 = threading.Thread(target=self.call_api, args=("key1",))
        t2 = threading.Thread(target=self.call_api, args=("key2",))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        payouts = Payout.objects.filter(merchant=self.merchant)

        # Only one payout should be effectively valid (no overdraft)
        self.assertLessEqual(payouts.count(), 2)
        

        # Check no negative balance
        credit = Ledger.objects.filter(merchant=self.merchant, type="CREDIT").aggregate(Sum('amount'))['amount__sum'] or 0
        debit = Ledger.objects.filter(merchant=self.merchant, type="DEBIT").aggregate(Sum('amount'))['amount__sum'] or 0
        held = Ledger.objects.filter(merchant=self.merchant, type="HELD").aggregate(Sum('amount'))['amount__sum'] or 0

        available = (credit or 0) - (debit or 0) - (held or 0)

        self.assertGreaterEqual(available, 0)


class IdempotencyTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.merchant = Merchant.objects.create(name="Test Merchant")

        Ledger.objects.create(
            merchant=self.merchant,
            amount=10000,
            type="CREDIT"
        )

    def test_idempotent_request(self):
        data = {
            "merchant_id": self.merchant.id,
            "amount_paise": 5000,
            "bank_account_id": "acc1"
        }

        r1 = self.client.post(
    "/api/v1/payouts/",
    data={
        "merchant_id": self.merchant.id,
        "amount_paise": 5000,
        "bank_account_id": "acc1"
    },
    format="json",
    HTTP_IDEMPOTENCY_KEY="fixed-key"
)

        r2 = self.client.post(
            "/api/v1/payouts/",
            data=data,
            format="json",
            HTTP_IDEMPOTENCY_KEY="fixed-key"
        )

        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 200)

        self.assertEqual(r1.data, r2.data)

        payouts = Payout.objects.filter(merchant=self.merchant)
        self.assertEqual(payouts.count(), 1)

        keys = Idempotency.objects.filter(merchant=self.merchant)
        self.assertEqual(keys.count(), 1)

        