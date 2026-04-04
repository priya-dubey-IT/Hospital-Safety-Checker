from fastapi import APIRouter, HTTPException, status
from app.models.schemas import PatientOnlyRequest
from app.database_sqlite import db
from app.services.face_service import process_face_image

router = APIRouter(prefix="/api/patient", tags=["Patient"])

@router.post("/register")
async def register_patient_only(request: PatientOnlyRequest):
    """
    Register a patient for an existing doctor
    """
    try:
        # Find doctor by name
        doctor = await db.get_doctor_by_name(request.doctor_name)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Doctor '{request.doctor_name}' not found"
            )
        
        # Process patient face if provided (Restored for patient page)
        patient_face_encoding = None
        if request.patient_face_image:
            patient_face_encoding = await process_face_image(request.patient_face_image)
            
            # Check if patient already exists by face
            existing = await db.find_patient_by_face(patient_face_encoding)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Patient with this face already registered: {existing.get('name')}"
                )
        
        # Create patient
        patient_id = await db.create_patient(
            name=request.patient_name,
            face_embedding=patient_face_encoding
        )
        
        # Create assignment
        assignment_id = await db.create_assignment(
            doctor_id=doctor['id'],
            patient_id=patient_id,
            status="waiting"
        )
        
        return {
            "success": True,
            "message": "Patient registered successfully",
            "patient_id": patient_id,
            "assignment_id": assignment_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Patient registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Patient registration failed: {str(e)}"
        )

@router.get("/doctors")
async def get_doctors():
    """
    Get list of all registered doctors
    """
    try:
        doctors = await db.get_all_doctors()
        # Remove face embeddings from response (too large)
        for doctor in doctors:
            if 'face_embedding' in doctor:
                doctor['has_face'] = True
                del doctor['face_embedding']
        
        return {
            "success": True,
            "doctors": doctors
        }
    except Exception as e:
        print(f"Get doctors error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get doctors: {str(e)}"
        )
