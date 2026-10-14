# Integration Setup & Troubleshooting

## Setup
1. Copy .env.example to .env
2. Set INTEGRATION_MOCK=True for local dev (no real API calls)
3. For production: Set real keys and INTEGRATION_MOCK=False

## Endpoints Covered
- SMS: POST https://api.msg91.com/api/v5/flow/ (Timeout 5s, Retry 3x)
- Payment: POST https://api.razorpay.com/v1/orders (Timeout 10s)

## Failure Handling
- Invalid mobile -> IntegrationError (400-level)
- Timeout -> Retried 3 times with exponential backoff (2s,4s,8s)
- Secrets never logged - only status code + first 200 chars of body

## Testing
python manage.py test apps.integrations -v 2
- Positive: mock success
- Negative: invalid mobile, invalid amount, timeout

## Demo
SMSService().send_otp("9876543210","1234") -> success in mock mode
