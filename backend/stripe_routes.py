import os
import stripe
from fastapi import APIRouter, Request, HTTPException

router = APIRouter()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_placeholder")

@router.post("/create-checkout-session")
async def create_checkout_session(tier: str):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': 'price_placeholder', # need actual price id based on tier
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:3000/dashboard?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/pricing',
        )
        return {"id": session.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_placeholder")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # fulfill order
        print(f"Checkout session completed: {session.id}")

    return {"status": "success"}
