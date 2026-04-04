try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("WARNING: face_recognition library not available. Using mock service for demo.")
    print("   For production, install: pip install cmake dlib face-recognition")

import numpy as np
import base64
import io
from PIL import Image
from typing import Optional, List, Tuple
from app.config import settings
import hashlib

class FaceRecognitionService:
    """
    Service for face recognition operations using face_recognition library
    """
    
    @staticmethod
    def base64_to_image(base64_string: str) -> np.ndarray:
        """
        Convert base64 string to numpy array image
        
        Args:
            base64_string: Base64 encoded image string
            
        Returns:
            numpy array image in RGB format
        """
        try:
            # Remove data URL prefix if present
            if "," in base64_string:
                base64_string = base64_string.split(",")[1]
            
            # Decode base64 to bytes
            image_bytes = base64.b64decode(base64_string)
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            return np.array(image)
        except Exception as e:
            raise ValueError(f"Failed to decode image: {str(e)}")
    
    @staticmethod
    def get_face_encoding(image: np.ndarray) -> Optional[List[float]]:
        """
        Extract face encoding from image
        
        Args:
            image: numpy array image in RGB format
            
        Returns:
            List of 128 face encoding values or None if no face found
        """
        try:
            if FACE_RECOGNITION_AVAILABLE:
                # Use real face recognition
                face_locations = face_recognition.face_locations(
                    image, 
                    model=settings.FACE_MODEL
                )
                
                if not face_locations:
                    return None
                
                face_encodings = face_recognition.face_encodings(
                    image, 
                    face_locations
                )
                
                if not face_encodings:
                    return None
                
                return face_encodings[0].tolist()
            else:
                # Use mock hash-based encoding for demo
                # Resize image to standard size for consistency
                from PIL import Image as PILImage
                pil_img = PILImage.fromarray(image)
                pil_img = pil_img.resize((128, 128))  # Standard size
                
                # Convert to grayscale for better consistency
                pil_img = pil_img.convert('L')
                img_array = np.array(pil_img)
                
                # Create encoding from image statistics (more robust than raw hash)
                encoding = []
                
                # Divide image into 8x8 blocks and get average
                block_size = 16
                for i in range(0, 128, block_size):
                    for j in range(0, 128, block_size):
                        block = img_array[i:i+block_size, j:j+block_size]
                        avg = float(np.mean(block)) / 255.0
                        encoding.append(avg)
                
                # Pad to 128 dimensions
                while len(encoding) < 128:
                    encoding.append(0.0)
                encoding = encoding[:128]
                
                return encoding
        except Exception as e:
            raise ValueError(f"Failed to extract face encoding: {str(e)}")
    
    @staticmethod
    def compare_faces(known_encoding: List[float], 
                     unknown_encoding: List[float]) -> Tuple[bool, float]:
        """
        Compare two face encodings
        
        Args:
            known_encoding: Known face encoding
            unknown_encoding: Unknown face encoding to compare
            
        Returns:
            Tuple of (is_match: bool, distance: float)
        """
    @staticmethod
    def compare_faces(known_encoding: List[float], 
                     unknown_encoding: List[float]) -> Tuple[bool, float]:
        """
        Compare two face encodings
        
        Args:
            known_encoding: Known face encoding
            unknown_encoding: Unknown face encoding to compare
            
        Returns:
            Tuple of (is_match: bool, distance: float)
        """
        try:
            if FACE_RECOGNITION_AVAILABLE:
                # Use real face recognition
                # Convert lists to numpy arrays if they aren't already
                known_array = np.array(known_encoding)
                unknown_array = np.array(unknown_encoding)
                
                distance = face_recognition.face_distance(
                    [known_array], 
                    unknown_array
                )[0]
                
                is_match = distance <= settings.FACE_TOLERANCE
                return is_match, float(distance)
            else:
                # Use mock comparison (euclidean distance)
                distance = sum((a - b) ** 2 for a, b in zip(known_encoding, unknown_encoding)) ** 0.5
                distance = distance / 128.0
                # Stricter threshold - only match if very similar
                is_match = distance < 0.05  # Reduced from 0.15 to be more strict
                return is_match, float(distance)
        except Exception as e:
            raise ValueError(f"Failed to compare faces: {str(e)}")
    
    @staticmethod
    async def find_matching_face(face_encoding: List[float], 
                                 collection, 
                                 field_name: str = "face_embedding") -> Optional[dict]:
        """
        Find matching face in database collection
        
        Args:
            face_encoding: Face encoding to search for
            collection: MongoDB collection to search
            field_name: Name of the field containing face embeddings
            
        Returns:
            Matching document or None
        """
        try:
            # Get all documents with face embeddings
            cursor = collection.find({field_name: {"$exists": True, "$ne": None}})
            documents = await cursor.to_list(length=None)
            
            # Compare with each stored face
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

# Convenience function
async def process_face_image(base64_image: str) -> Optional[List[float]]:
    """
    Process base64 image and extract face encoding
    
    Args:
        base64_image: Base64 encoded image
        
    Returns:
        Face encoding or None
    """
    if not base64_image:
        return None
    
    image = FaceRecognitionService.base64_to_image(base64_image)
    encoding = FaceRecognitionService.get_face_encoding(image)
    
    if encoding is None:
        raise ValueError("No face detected in image")
    
    return encoding
