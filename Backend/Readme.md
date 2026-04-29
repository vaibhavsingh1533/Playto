Payout Processing System

A full-stack system that allows merchants to view balances, request payouts, and track payout status with strong guarantees around idempotency, concurrency, and data integrity.

Tech Stack
Backend: Django + Django REST Framework
Database: PostgreSQL
Async Processing: Celery + Redis
Frontend: React + Tailwind CSS
Features

1. Merchant Ledger
All amounts stored in paise (integer)
Balance derived from:
CREDIT (incoming funds)
DEBIT (completed payouts)
HELD (pending payouts)
Available balance = CREDIT − DEBIT − HELD

2. Payout Request API

POST /api/v1/payouts/

Headers:

Idempotency-Key: unique_key

Body:

{
  "merchant_id": 1,
  "amount_paise": 5000,
  "bank_account_id": "demo_account_1"
}
Creates payout in PENDING
Funds are HELD immediately
Same idempotency key → same response (no duplicate payouts)

3. Payout Processor (Celery Worker)
Processes payouts asynchronously
Simulates bank behavior:
70% → SUCCESS
20% → FAILED
10% → PROCESSING (retry)

Lifecycle:

PENDING → PROCESSING → SUCCESS / FAILED
SUCCESS → HELD → DEBIT
FAILED → funds released (no debit)

4. Merchant Dashboard (React)
Available balance
Held balance
Payout request form
Payout history (live updates)
Ledger history (credits, debits, held)


Running the Project
1. Backend
python manage.py runserver
2. Frontend
cd frontend
npm start
3. Redis
redis-server
4. Celery Worker
celery -A core worker -l info --pool=solo
Key Concepts Implemented
Idempotency

Prevents duplicate payouts using a unique key per request.

Concurrency Control

Uses select_for_update() and database transactions to avoid race conditions.

Data Integrity

Atomic transactions ensure balance consistency.

Async Processing

Background jobs handled via Celery + Redis.

Project Structure
backend/
  core/
  payout/
frontend/
README.md


Future Improvements
Authentication (JWT)
Retry backoff strategy
WebSockets for real-time updates
Deployment (Docker + Cloud)