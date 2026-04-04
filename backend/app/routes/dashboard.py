from fastapi import APIRouter, HTTPException, status
from app.database_sqlite import db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/waiting")
async def get_waiting_list():
    """
    Get all waiting assignments
    """
    try:
        assignments = await db.get_waiting_assignments()
        return {
            "success": True,
            "assignments": assignments
        }
    except Exception as e:
        print(f"Get waiting list error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get waiting list: {str(e)}"
        )

@router.get("/completed")
async def get_completed_list():
    """
    Get all completed assignments
    """
    try:
        assignments = await db.get_completed_assignments()
        return {
            "success": True,
            "assignments": assignments
        }
    except Exception as e:
        print(f"Get completed list error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get completed list: {str(e)}"
        )

@router.get("/doctor/{doctor_id}/waiting")
async def get_doctor_waiting_list(doctor_id: int):
    """
    Get waiting assignments for a specific doctor
    """
    try:
        assignments = await db.get_waiting_assignments_by_doctor(doctor_id)
        return {
            "success": True,
            "assignments": assignments
        }
    except Exception as e:
        print(f"Get doctor waiting list error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get doctor waiting list: {str(e)}"
        )

@router.get("/doctor/{doctor_id}/completed")
async def get_doctor_completed_list(doctor_id: int):
    """
    Get completed assignments for a specific doctor
    """
    try:
        assignments = await db.get_completed_assignments_by_doctor(doctor_id)
        return {
            "success": True,
            "assignments": assignments
        }
    except Exception as e:
        print(f"Get doctor completed list error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get doctor completed list: {str(e)}"
        )

@router.put("/complete/{assignment_id}")
async def mark_as_complete(assignment_id: int):
    """
    Mark assignment as complete
    """
    try:
        assignment = await db.get_assignment_by_id(assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        await db.update_assignment_status(assignment_id, "completed")
        
        return {
            "success": True,
            "message": "Assignment marked as complete"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Mark complete error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark as complete: {str(e)}"
        )

@router.delete("/delete/{assignment_id}")
async def delete_assignment(assignment_id: int):
    """
    Delete an assignment
    """
    try:
        assignment = await db.get_assignment_by_id(assignment_id)
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        await db.delete_assignment(assignment_id)
        
        return {
            "success": True,
            "message": "Assignment deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete assignment error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete assignment: {str(e)}"
        )
