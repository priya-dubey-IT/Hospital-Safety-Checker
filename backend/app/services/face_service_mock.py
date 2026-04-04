# Mock face recognition service for demo purposes
# This allows the app to run without face_recognition library
import base64
import io
import hashlib
from PIL import Image
import numpy as np
from typing import Optional, List, Tuple

class FaceRecognitionService:
    """
    Mock service for face recognition (for demo without face_recognition library)
    In production, install face_recognition library for real biometric matching
    """
    
    @staticmethod
    def base64_to_image(base64_string: str) -> np.ndarray:
        """Convert base64 string to numpy array image"""
        try:
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]
            
            image_bytes = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_bytes))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            return np.array(image)
        except Exception as e:
            raise ValueError(f"Failed to decode image: {str(e)}")
    
    @staticmethod
    def get_face_encoding(image: np.ndarray) -> Optional[List[float]]:
        """
        Mock face encoding - creates a hash-based encoding
        NOTE: This is NOT real face recognition! For demo only.
        """
        try:
            # Create a simple hash-based encoding (128 dimensions)
            image_hash = hashlib.sha256(image.tobytes()).hexdigest()
            # Convert hex to 128 float values
            encoding = [float(int(image_hash[i:i+2], 16)) / 255.0 for i in range(0, 128, 1)]
            encoding = encoding[:128]  # Ensure exactly 128 dimensions
            # Pad if needed
            while len(encoding) < 128:
                encoding.append(0.0)
            return encoding
        except Exception as e:
            raise ValueError(f"Failed to extract face encoding: {str(e)}")
    
    @staticmethod
    def compare_faces(known_encoding: List[float], 
                     unknown_encoding: List[float]) -> Tuple[bool, float]:
        """
        Mock face comparison - compares hash-based encodings
        NOTE: This is NOT real face recognition! For demo only.
        """
        try:
            # Calculate simple euclidean distance
            distance = sum((a - b) ** 2 for a, b in zip(known_encoding, unknown_encoding)) ** 0.5
            # Normalize distance
            distance = distance / 128.0
            
            # Very strict matching for hash-based system
            is_match = distance < 0.01  # Almost identical
            
            return is_match, float(distance)
        except Exception as e:
            raise ValueError(f"Failed to compare faces: {str(e)}")
    
    @staticmethod
    async def find_matching_face(face_encoding: List[float], 
                                 collection, 
                                 field_name: str = "face_embedding") -> Optional[dict]:
        """Find matching face in database collection"""
        try:
            cursor = collection.find({field_name: {"$exists": True, "$ne": None}})
            documents = await cursor.to_list(length=None)
            
            for doc in documents:
                stored_encoding = doc.get(field_name)
                if stored_encoding:
                    is_match, distance = FaceRecognitionService.compare_faces(
                        stored_encoding, 
                        face_encoding
                    )
                    if is_match:
                        return doc
            
            return None
        except Exception as e:
            raise ValueError(f"Failed to find matching face: {str(e)}")

async def process_face_image(base64_image: str) -> Optional[List[float]]:
    """Process base64 image and extract face encoding"""
    if not base64_image:
        return None
    
    image = FaceRecognitionService.base64_to_image(base64_image)
    encoding = FaceRecognitionService.get_face_encoding(image)
    
    if encoding is None:
        raise ValueError("No face detected in image")
    
    return encoding
