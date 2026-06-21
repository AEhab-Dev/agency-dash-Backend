from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.services.stripe_service import create_checkout_session, handle_webhook

router = APIRouter(prefix="/api/payments", tags=["payments"])


@router.post("/create-checkout")
def create_checkout(
    current_user: User = Depends(get_current_user),
):
    url = create_checkout_session(current_user)
    return {"url": url}


@router.post("/webhook")
async def webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    handle_webhook(payload, sig_header, db)
    return {"detail": "Webhook received"}