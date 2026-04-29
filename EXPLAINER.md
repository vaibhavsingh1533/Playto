EXPLAINER
1. The Ledger
Balance Calculation
from django.db.models import Sum

credit = Ledger.objects.filter(merchant=merchant, type="CREDIT").aggregate(Sum('amount'))['amount__sum'] or 0
debit = Ledger.objects.filter(merchant=merchant, type="DEBIT").aggregate(Sum('amount'))['amount__sum'] or 0
held = Ledger.objects.filter(merchant=merchant, type="HELD").aggregate(Sum('amount'))['amount__sum'] or 0

available_balance = credit - debit - held
Why this design?

Instead of storing a balance directly, I used a ledger-based model where all transactions are recorded as entries (CREDIT, DEBIT, HELD).

This ensures:

Auditability — every change is traceable
Consistency — no risk of stale balance values
Financial correctness — pending payouts (HELD) are accounted for
2. The Lock
Ledger.objects.select_for_update().filter(merchant=merchant)
Explanation

This uses PostgreSQL row-level locking inside a database transaction.

Prevents multiple concurrent requests from reading the same balance
Ensures only one payout can modify the ledger at a time
Avoids race conditions and double spending
3. The Idempotency
existing = Idempotency.objects.filter(key=key, merchant=merchant).first()
How it works
Each request includes an Idempotency-Key
If the key already exists, the stored response is returned
Concurrent request scenario

If two identical requests arrive at the same time:

First request processes and stores the response
Second request finds the existing key and returns the same response

This guarantees no duplicate payouts.

4. The State Machine
if payout.status not in ["PENDING", "PROCESSING"]:
    return
Explanation

This enforces valid state transitions:

PENDING → PROCESSING → SUCCESS / FAILED
Prevents invalid transitions like FAILED → SUCCESS
Ensures payout lifecycle remains consistent
5. The AI Audit
AI Suggested (Incorrect)
balance = credit - debit
Issue

This ignored HELD funds, allowing payouts to exceed available balance.

Fixed Implementation
balance = credit - debit - held
Why this matters

HELD funds represent pending payouts and must be excluded from available balance to prevent overspending.

Summary

This system ensures:

Concurrency safety using database locks
Idempotency to prevent duplicate payouts
Data integrity through atomic transactions
Financial correctness with a ledger-based model
Scalable processing using Celery background workers