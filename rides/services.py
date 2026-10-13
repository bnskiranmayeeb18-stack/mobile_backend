import random, time
from .models import Payment

def mock_process_payment(payment: Payment):
    # Simulate processing
    time.sleep(1)
    # 80% success
    if random.random() < 0.8:
        return Payment.Status.SUCCESS
    return Payment.Status.FAILED