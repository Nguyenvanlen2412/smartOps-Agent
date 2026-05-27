from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from mock_api.mock_db import USERS
from datetime import datetime

router = APIRouter(
    prefix="/emails",
    tags=["Emails"]
)

class EmailRequest(BaseModel):
    user_id: str
    subject: str
    message: str
@router.post("/notify")
def notify_email(request: EmailRequest):
    user = USERS.get(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Simulate sending email (in real implementation, integrate with email service)
    print(f"Email sent to {user['name']} ({user['email']}) - Subject: {request.subject}")
    print(f"Message: {request.message}")
    
    return {
        "recipient_name": user["name"],
        "recipient_email": user["email"],
        "subject": request.subject,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }