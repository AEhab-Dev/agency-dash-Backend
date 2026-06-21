import stripe
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.core.config import settings
from app.models.user import User

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(user: User) -> str:
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            customer_email=user.email,
            line_items=[
                {
                    "price": settings.STRIPE_PRICE_ID,
                    "quantity": 1,
                }
            ],
            success_url=f"{settings.FRONTEND_URL}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.FRONTEND_URL}/projects",
            metadata={"user_id": str(user.id)},
        )
        return session.url
    except stripe.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


def handle_webhook(payload: bytes, sig_header: str, db: Session) -> None:
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid webhook signature",
        )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = int(session["metadata"]["user_id"])
        subscription_id = session.get("subscription")
        customer_id = session.get("customer")

        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.plan = "paid"
            user.stripe_subscription_id = subscription_id
            user.stripe_customer_id = customer_id
            db.commit()