"""
Service for exporting data to Excel format
"""
import pandas as pd
from datetime import datetime
import os
from typing import List, Dict

class ExcelService:
    """Service for handling Excel export operations"""
    
    @staticmethod
    async def export_to_excel(doctors: List[Dict], patients: List[Dict], assignments: List[Dict]) -> str:
        """
        Export all data to Excel with combined doctor-patient information
        
        Args:
            doctors: List of doctor records
            patients: List of patient records
            assignments: List of assignment records
            
        Returns:
            Path to the created Excel file
        """
        # Create combined data
        combined_data = []
        
        # Helper function to format dates
        def format_date(date_str):
            if not date_str:
                return ''
            try:
                # Parse ISO format date
                dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                return date_str
        
        for assignment in assignments:
            # Find matching doctor
            doctor = next((d for d in doctors if d['id'] == assignment['doctor_id']), None)
            # Find matching patient
            patient = next((p for p in patients if p['id'] == assignment['patient_id']), None)
            
            if doctor and patient:
                combined_data.append({
                    'ID': assignment.get('id', ''),
                    'Doctor Name': doctor.get('name', ''),
                    'Category': doctor.get('category', ''),
                    'Doctor Face Recognition': 'Yes' if doctor.get('has_face', False) else 'No',
                    'Doctor Fingerprint': 'Yes' if doctor.get('fingerprint_hash') else 'No',
                    'Patient Name': patient.get('name', ''),
                    'Patient Face Recognition': 'Yes' if patient.get('has_face', False) else 'No',
                    'Patient Fingerprint': 'Yes' if patient.get('fingerprint_hash') else 'No',
                    'Registered Date': format_date(assignment.get('timestamp', '')),
                    'End Session': format_date(assignment.get('completed_at', '')) if assignment.get('status') == 'completed' else ''
                })
        
        # Create DataFrame
        df = pd.DataFrame(combined_data)
        
        # Create exports directory if it doesn't exist
        exports_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(exports_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hospital_data_{timestamp}.xlsx"
        filepath = os.path.join(exports_dir, filename)
        
        # Write to Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Hospital Data', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Hospital Data']
            for idx, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = max_length
        
        return filepath
