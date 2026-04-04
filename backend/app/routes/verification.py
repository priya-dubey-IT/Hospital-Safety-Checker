from fastapi import APIRouter, HTTPException, status
from app.models.schemas import VerificationRequest
from app.database_sqlite import db
from app.services.face_service import process_face_image
from app.services.fingerprint_service import FingerprintService

router = APIRouter(prefix="/api/verification", tags=["Verification"])

@router.post("/verify")
async def verify_doctor(request: VerificationRequest):
    """
    Verify doctor using face or fingerprint
    """
    try:
        doctor = None
        verification_method = None
        
        # Biometric verification removed - using name-based only
        if request.doctor_name:
            doctor = await db.get_doctor_by_name(request.doctor_name)
            if doctor:
                verification_method = "name"
        
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found. Please check your biometric data."
            )
        
        # Get doctor's assignments
        assignments = await db.get_assignments_by_doctor(doctor['id'])
        
        # Enrich assignments with patient data
        enriched_assignments = []
        for assignment in assignments:
            patient = await db.get_patient_by_id(assignment['patient_id'])
            enriched_assignments.append({
                "patient_id": patient['id'],
                "patient_name": patient['name'],
                "status": assignment['status']
            })
            
        waiting_count = sum(1 for a in assignments if a['status'] == 'waiting')
        
        return {
            "success": True,
            "message": "Verification successful",
            "doctor": {
                "id": doctor['id'],
                "name": doctor['name'],
                "category": doctor['category']
            },
            "verification_method": verification_method,
            "waiting_patients": waiting_count,
            "assignments": enriched_assignments
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Verification failed: {str(e)}"
        )
