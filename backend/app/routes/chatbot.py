from fastapi import APIRouter, HTTPException, status
from app.models.schemas import ChatbotRequest
from app.database_sqlite import db
import uuid

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])

@router.post("/chat")
async def chat(request: ChatbotRequest):
    """
    Chat with the hospital assistant bot
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Simple rule-based responses
        message_lower = request.message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey']):
            response = "Hello! I'm your Hospital Safety Checker assistant. How can I help you today?"
        elif 'register' in message_lower:
            response = "To register, go to the Registration page and fill in the doctor and patient details with biometric data (face/fingerprint)."
        elif 'verify' in message_lower or 'verification' in message_lower:
            response = "For verification, go to the Verification page and provide your face image or fingerprint to verify your identity as a doctor."
        elif 'dashboard' in message_lower:
            response = "The Dashboard shows waiting and completed patient assignments. You can mark assignments as complete or delete them."
        elif 'admin' in message_lower:
            response = "The Admin panel allows you to view all doctors, patients, and assignments. You can also export data to Excel."
        elif 'patient' in message_lower:
            response = "You can register patients individually on the Patient Registration page by selecting an existing doctor."
        elif 'help' in message_lower or 'how' in message_lower:
            response = "I can help you with:\n• Registration process\n• Doctor verification\n• Dashboard usage\n• Admin panel features\n• Patient management\n\nWhat would you like to know more about?"
        else:
            response = "I'm here to help! You can ask me about registration, verification, dashboard, admin panel, or patient management."
        
        # Save to database
        await db.save_chat_message(session_id, request.message, response)
        
        return {
            "success": True,
            "response": response,
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

@router.get("/history")
async def get_history(session_id: str = "default"):
    """
    Get chat history for a session
    """
    try:
        history = await db.get_chat_history(session_id)
        return {
            "success": True,
            "history": history
        }
    except Exception as e:
        print(f"Get history error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get history: {str(e)}"
        )
