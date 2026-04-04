from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.database_sqlite import db
from app.services.excel_service import ExcelService
import os

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/doctors")
async def get_all_doctors():
    """
    Get all doctors for admin panel
    """
    try:
        doctors = await db.get_all_doctors()
        # Remove face embeddings
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

@router.get("/patients")
async def get_all_patients():
    """
    Get all patients for admin panel
    """
    try:
        patients = await db.get_all_patients()
        # Remove face embeddings
        for patient in patients:
            if 'face_embedding' in patient:
                patient['has_face'] = True
                del patient['face_embedding']
        
        return {
            "success": True,
            "patients": patients
        }
    except Exception as e:
        print(f"Get patients error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get patients: {str(e)}"
        )

@router.get("/assignments")
async def get_all_assignments():
    """
    Get all assignments for admin panel
    """
    try:
        assignments = await db.get_all_assignments()
        return {
            "success": True,
            "assignments": assignments
        }
    except Exception as e:
        print(f"Get assignments error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get assignments: {str(e)}"
        )

@router.delete("/doctors/{doctor_id}")
async def delete_doctor(doctor_id: int):
    """
    Delete a doctor
    """
    try:
        doctor = await db.get_doctor_by_id(doctor_id)
        if not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Doctor not found"
            )
        
        await db.delete_doctor(doctor_id)
        
        return {
            "success": True,
            "message": "Doctor deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete doctor error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete doctor: {str(e)}"
        )

@router.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int):
    """
    Delete a patient
    """
    try:
        patient = await db.get_patient_by_id(patient_id)
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found"
            )
        
        await db.delete_patient(patient_id)
        
        return {
            "success": True,
            "message": "Patient deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete patient error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete patient: {str(e)}"
        )

@router.get("/export/excel")
async def export_to_excel():
    """
    Export all data to Excel
    """
    try:
        doctors = await db.get_all_doctors()
        patients = await db.get_all_patients()
        assignments = await db.get_all_assignments()
        
        
        # Mark has_face before removing embeddings
        for doctor in doctors:
            if 'face_embedding' in doctor:
                doctor['has_face'] = True
                del doctor['face_embedding']
            else:
                doctor['has_face'] = False
                
        for patient in patients:
            if 'face_embedding' in patient:
                patient['has_face'] = True
                del patient['face_embedding']
            else:
                patient['has_face'] = False
        
        file_path = await ExcelService.export_to_excel(doctors, patients, assignments)
        
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create Excel file"
            )
        
        return FileResponse(
            path=file_path,
            filename="hospital_data.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Export error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export failed: {str(e)}"
        )
