from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import core_schema
from typing import Optional, List, Any
from datetime import datetime
from bson import ObjectId

class PyObjectId(str):
    """Custom ObjectId type for Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler):
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ],
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda x: str(x)
        ))
    
    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")


class DoctorModel(BaseModel):
    """Doctor data model"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    category: str
    face_embedding: Optional[List[float]] = None
    fingerprint_hash: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PatientModel(BaseModel):
    """Patient data model"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    face_embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AssignmentModel(BaseModel):
    """Doctor-Patient assignment model"""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    doctor_id: str
    patient_id: str
    status: str = "waiting"  # waiting or completed
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class RegistrationRequest(BaseModel):
    """Request model for main registration"""
    doctor_name: str
    doctor_category: str
    doctor_face_image: Optional[str] = None  # base64 encoded
    doctor_fingerprint: Optional[str] = None
    patient_name: str
    patient_face_image: Optional[str] = None  # base64 encoded

class PatientOnlyRequest(BaseModel):
    """Request model for patient-only registration"""
    doctor_name: str
    patient_name: str
    patient_face_image: Optional[str] = None  # base64 encoded

class VerificationRequest(BaseModel):
    """Request model for doctor verification"""
    doctor_name: str
    face_image: Optional[str] = None  # base64 encoded
    fingerprint: Optional[str] = None

class ChatbotRequest(BaseModel):
    """Request model for chatbot"""
    message: str
    session_id: Optional[str] = None
