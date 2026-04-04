from fastapi import APIRouter, HTTPException, status
from app.models.schemas import RegistrationRequest
from app.database_sqlite import db
from app.services.face_service import process_face_image
from app.services.fingerprint_service import FingerprintService

router = APIRouter(prefix="/api/registration", tags=["Registration"])

@router.post("/main")
async def main_registration(request: RegistrationRequest):
    """
    Main registration endpoint for both doctor and patient
    
    Validates that biometrics are not already registered
    Creates doctor and patient records
    Creates assignment mapping
    """
    try:
        # Biometric processing removed as per request to remove image option
        doctor_face_encoding = None
        doctor_fingerprint_hash = None
        patient_face_encoding = None
        
        # No longer required if "normal" registration is used
        # if not patient_face_encoding:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Face image is required for patient"
        #     )
        
        # Create doctor record
        doctor_id = await db.create_doctor(
            name=request.doctor_name,
            category=request.doctor_category,
            face_embedding=doctor_face_encoding,
            fingerprint_hash=doctor_fingerprint_hash
        )
        
        # Create patient record
        patient_id = await db.create_patient(
            name=request.patient_name,
            face_embedding=patient_face_encoding
        )
        
        # Create assignment
        assignment_id = await db.create_assignment(
            doctor_id=doctor_id,
            patient_id=patient_id,
            status="waiting"
        )
        
        return {
            "success": True,
            "message": "Registration successful",
            "doctor_id": doctor_id,
            "patient_id": patient_id,
            "assignment_id": assignment_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )
