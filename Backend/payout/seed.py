from payout.models import Merchant, Ledger

def run():
    # Create merchants
    m1 = Merchant.objects.create(name="Merchant A")
    m2 = Merchant.objects.create(name="Merchant B")

    # Add balance (credits)
    Ledger.objects.create(merchant=m1, amount=20000, type="CREDIT")
    Ledger.objects.create(merchant=m1, amount=10000, type="CREDIT")

    Ledger.objects.create(merchant=m2, amount=50000, type="CREDIT")

    print("Seed data created successfully!")