"""
API routes for patient medical reports
"""
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.database_sqlite import db
from app.services.report_service import ReportService
import os

router = APIRouter(prefix="/api/reports", tags=["Reports"])

class ReportCreateRequest(BaseModel):
    assignment_id: int
    patient_age: str = ""
    patient_gender: str = ""
    diagnosis: str = ""
    symptoms: str = ""
    treatment: str = ""
    medications: str = ""
    notes: str = ""

class ReportUpdateRequest(BaseModel):
    patient_age: str = None
    patient_gender: str = None
    diagnosis: str = None
    symptoms: str = None
    treatment: str = None
    medications: str = None
    notes: str = None

@router.post("/create")
async def create_report(request: ReportCreateRequest):
    """Create a new patient report"""
    try:
        # Get assignment details
        assignment = await db.get_assignment_by_id(request.assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Check if report already exists
        existing_report = await db.get_report_by_assignment(request.assignment_id)
        if existing_report:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Report already exists for this assignment"
            )
        
        # Get patient and doctor details
        patient = await db.get_patient_by_id(assignment['patient_id'])
        doctor = await db.get_doctor_by_id(assignment['doctor_id'])
        
        if not patient or not doctor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient or doctor not found"
            )
        
        # Create report in database
        report_id = await db.create_report(
            assignment_id=request.assignment_id,
            patient_name=patient['name'],
            doctor_name=doctor['name'],
            patient_age=request.patient_age,
            patient_gender=request.patient_gender,
            diagnosis=request.diagnosis,
            symptoms=request.symptoms,
            treatment=request.treatment,
            medications=request.medications,
            notes=request.notes
        )
        
        return {
            "success": True,
            "message": "Report created successfully",
            "report_id": report_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Create report error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create report: {str(e)}"
        )

@router.get("/{assignment_id}")
async def get_report(assignment_id: int):
    """Get report by assignment ID"""
    try:
        report = await db.get_report_by_assignment(assignment_id)
        
        if not report:
            # Return empty report structure if not found
            assignment = await db.get_assignment_by_id(assignment_id)
            if not assignment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assignment not found"
                )
            
            patient = await db.get_patient_by_id(assignment['patient_id'])
            doctor = await db.get_doctor_by_id(assignment['doctor_id'])
            
            return {
                "success": True,
                "report": {
                    "assignment_id": assignment_id,
                    "patient_name": patient['name'] if patient else "",
                    "doctor_name": doctor['name'] if doctor else "",
                    "patient_age": "",
                    "patient_gender": "",
                    "diagnosis": "",
                    "symptoms": "",
                    "treatment": "",
                    "medications": "",
                    "notes": "",
                    "exists": False
                }
            }
        
        report['exists'] = True
        return {
            "success": True,
            "report": report
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get report error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get report: {str(e)}"
        )

@router.put("/{assignment_id}")
async def update_report(assignment_id: int, request: ReportUpdateRequest):
    """Update an existing report"""
    try:
        # Check if report exists
        report = await db.get_report_by_assignment(assignment_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        # Build update dict from non-None values
        update_data = {
            k: v for k, v in request.dict().items() 
            if v is not None
        }
        
        if update_data:
            await db.update_report(assignment_id, **update_data)
        
        return {
            "success": True,
            "message": "Report updated successfully"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update report error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update report: {str(e)}"
        )

@router.get("/{assignment_id}/download")
async def download_report(assignment_id: int):
    """Download report as Word document"""
    try:
        # Get report from database
        report = await db.get_report_by_assignment(assignment_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found. Please create the report first."
            )
        
        
        # Get assignment to get the registration timestamp and IDs
        assignment = await db.get_assignment_by_id(assignment_id)
        if assignment:
            # Add assignment timestamp as registration_date
            report['registration_date'] = assignment.get('timestamp')
            
            # Get doctor and patient for photos
            doctor = await db.get_doctor_by_id(assignment['doctor_id'])
            patient = await db.get_patient_by_id(assignment['patient_id'])
            
            # Add photo paths if they exist
            if doctor and doctor.get('photo_path'):
                report['doctor_photo'] = doctor.get('photo_path')
            if patient and patient.get('photo_path'):
                report['patient_photo'] = patient.get('photo_path')
        
        # Generate Word document
        filepath = ReportService.create_report_document(report)
        
        if not os.path.exists(filepath):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate report document"
            )
        
        return FileResponse(
            path=filepath,
            filename=os.path.basename(filepath),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Download report error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download report: {str(e)}"
        )
