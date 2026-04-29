from django.db import models

class Merchant(models.Model):
    name = models.CharField(max_length=100)


class Ledger(models.Model):
    TYPE_CHOICES = [
        ('CREDIT', 'Credit'),
        ('DEBIT', 'Debit'),
        ('HELD', 'Held')
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)


class Payout(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.BigIntegerField()
    bank_account_id = models.CharField(max_length=100)   # ✅ HERE
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    idempotency_key = models.CharField(max_length=100)
    retries = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Idempotency(models.Model):
    key = models.CharField(max_length=100)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    response = models.JSONField(null=True)

    class Meta:
        unique_together = ('key', 'merchant')