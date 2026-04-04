import hashlib
from typing import Optional

class FingerprintService:
    """
    Service for fingerprint processing
    Note: This is a simplified implementation. In production, you would
    integrate with actual fingerprint hardware SDK.
    """
    
    @staticmethod
    def hash_fingerprint(fingerprint_data: str) -> str:
        """
        Create a hash of fingerprint data for storage
        
        Args:
            fingerprint_data: Raw fingerprint data (or simulated data)
            
        Returns:
            SHA256 hash of fingerprint
        """
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    @staticmethod
    def verify_fingerprint(stored_hash: str, input_data: str) -> bool:
        """
        Verify fingerprint against stored hash
        
        Args:
            stored_hash: Stored fingerprint hash
            input_data: Input fingerprint data to verify
            
        Returns:
            True if match, False otherwise
        """
        input_hash = FingerprintService.hash_fingerprint(input_data)
        return stored_hash == input_hash
    
    @staticmethod
    async def find_matching_fingerprint(fingerprint_hash: str, 
                                       collection) -> Optional[dict]:
        """
        Find matching fingerprint in database
        
        Args:
            fingerprint_hash: Fingerprint hash to search for
            collection: MongoDB collection to search
            
        Returns:
            Matching document or None
        """
        return await collection.find_one({"fingerprint_hash": fingerprint_hash})
