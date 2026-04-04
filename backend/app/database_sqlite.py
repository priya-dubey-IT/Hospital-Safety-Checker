"""
SQLite Database Module for Hospital Safety Checker
Replaces MongoDB with SQLite for easier setup
"""

import aiosqlite
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

class Database:
    def __init__(self, db_path: str = "hospital_safety.db"):
        self.db_path = db_path
        self.db = None
    
    async def connect(self):
        """Connect to SQLite database and create tables"""
        self.db = await aiosqlite.connect(self.db_path)
        self.db.row_factory = aiosqlite.Row
        await self.create_tables()
        print(f"Connected to SQLite database at {self.db_path}")
    
    async def close(self):
        """Close database connection"""
        if self.db:
            await self.db.close()
            print("Closed SQLite database connection")
    
    async def create_tables(self):
        """Create all necessary tables"""
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                face_embedding TEXT,
                fingerprint_hash TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                face_embedding TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                patient_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'waiting',
                timestamp TEXT NOT NULL,
                FOREIGN KEY (doctor_id) REFERENCES doctors (id),
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        """)
        
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS chatbot_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS patient_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER NOT NULL UNIQUE,
                patient_name TEXT NOT NULL,
                patient_age TEXT,
                patient_gender TEXT,
                diagnosis TEXT,
                symptoms TEXT,
                treatment TEXT,
                medications TEXT,
                notes TEXT,
                doctor_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (assignment_id) REFERENCES assignments (id)
            )
        """)
        
        await self.db.commit()
    
    # Doctor operations
    async def create_doctor(self, name: str, category: str, 
                          face_embedding: Optional[List[float]] = None,
                          fingerprint_hash: Optional[str] = None) -> int:
        """Create a new doctor"""
        face_json = json.dumps(face_embedding) if face_embedding else None
        created_at = datetime.utcnow().isoformat() + "Z"
        
        cursor = await self.db.execute(
            "INSERT INTO doctors (name, category, face_embedding, fingerprint_hash, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, category, face_json, fingerprint_hash, created_at)
        )
        await self.db.commit()
        return cursor.lastrowid
    
    async def get_doctor_by_id(self, doctor_id: int) -> Optional[Dict]:
        """Get doctor by ID"""
        cursor = await self.db.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    
    async def get_doctor_by_name(self, name: str) -> Optional[Dict]:
        """Get doctor by name"""
        cursor = await self.db.execute("SELECT * FROM doctors WHERE name = ?", (name,))
        row = await cursor.fetchone()
        if row:
            doc = dict(row)
            if doc.get('face_embedding'):
                doc['face_embedding'] = json.loads(doc['face_embedding'])
            return doc
        return None
    
    async def get_all_doctors(self) -> List[Dict]:
        """Get all doctors"""
        cursor = await self.db.execute("SELECT * FROM doctors ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        doctors = []
        for row in rows:
            doc = dict(row)
            if doc.get('face_embedding'):
                doc['face_embedding'] = json.loads(doc['face_embedding'])
            doctors.append(doc)
        return doctors
    
    async def delete_doctor(self, doctor_id: int):
        """Delete doctor and related assignments"""
        await self.db.execute("DELETE FROM assignments WHERE doctor_id = ?", (doctor_id,))
        await self.db.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        await self.db.commit()
    
    # Patient operations
    async def create_patient(self, name: str, face_embedding: Optional[List[float]] = None) -> int:
        """Create a new patient"""
        face_json = json.dumps(face_embedding) if face_embedding else None
        created_at = datetime.utcnow().isoformat() + "Z"
        
        cursor = await self.db.execute(
            "INSERT INTO patients (name, face_embedding, created_at) VALUES (?, ?, ?)",
            (name, face_json, created_at)
        )
        await self.db.commit()
        return cursor.lastrowid
    
    async def get_patient_by_id(self, patient_id: int) -> Optional[Dict]:
        """Get patient by ID"""
        cursor = await self.db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = await cursor.fetchone()
        if row:
            pat = dict(row)
            if pat.get('face_embedding'):
                pat['face_embedding'] = json.loads(pat['face_embedding'])
            return pat
        return None
    
    async def get_all_patients(self) -> List[Dict]:
        """Get all patients"""
        cursor = await self.db.execute("SELECT * FROM patients ORDER BY created_at DESC")
        rows = await cursor.fetchall()
        patients = []
        for row in rows:
            pat = dict(row)
            if pat.get('face_embedding'):
                pat['face_embedding'] = json.loads(pat['face_embedding'])
            patients.append(pat)
        return patients
    
    async def delete_patient(self, patient_id: int):
        """Delete patient and related assignments"""
        await self.db.execute("DELETE FROM assignments WHERE patient_id = ?", (patient_id,))
        await self.db.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        await self.db.commit()
    
    # Assignment operations
    async def create_assignment(self, doctor_id: int, patient_id: int, status: str = "waiting") -> int:
        """Create a new assignment"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        cursor = await self.db.execute(
            "INSERT INTO assignments (doctor_id, patient_id, status, timestamp) VALUES (?, ?, ?, ?)",
            (doctor_id, patient_id, status, timestamp)
        )
        await self.db.commit()
        return cursor.lastrowid
    
    async def get_assignment_by_id(self, assignment_id: int) -> Optional[Dict]:
        """Get assignment by ID"""
        cursor = await self.db.execute("SELECT * FROM assignments WHERE id = ?", (assignment_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
    
    async def get_assignments_by_doctor(self, doctor_id: int) -> List[Dict]:
        """Get all assignments for a doctor"""
        cursor = await self.db.execute(
            "SELECT * FROM assignments WHERE doctor_id = ? ORDER BY timestamp DESC",
            (doctor_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def get_waiting_assignments(self) -> List[Dict]:
        """Get all waiting assignments with doctor and patient info"""
        cursor = await self.db.execute("""
            SELECT a.id as assignment_id, a.status, a.timestamp,
                   d.id as doctor_id, d.name as doctor_name, d.category as doctor_category,
                   p.id as patient_id, p.name as patient_name
            FROM assignments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            WHERE a.status = 'waiting'
            ORDER BY a.timestamp DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def get_completed_assignments(self) -> List[Dict]:
        """Get all completed assignments with doctor and patient info"""
        cursor = await self.db.execute("""
            SELECT a.id as assignment_id, a.status, a.timestamp,
                   d.id as doctor_id, d.name as doctor_name, d.category as doctor_category,
                   p.id as patient_id, p.name as patient_name
            FROM assignments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            WHERE a.status = 'completed'
            ORDER BY a.timestamp DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def get_waiting_assignments_by_doctor(self, doctor_id: int) -> List[Dict]:
        """Get all waiting assignments for a specific doctor"""
        cursor = await self.db.execute("""
            SELECT a.id as assignment_id, a.status, a.timestamp,
                   d.id as doctor_id, d.name as doctor_name, d.category as doctor_category,
                   p.id as patient_id, p.name as patient_name
            FROM assignments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            WHERE a.status = 'waiting' AND a.doctor_id = ?
            ORDER BY a.timestamp DESC
        """, (doctor_id,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

    async def get_completed_assignments_by_doctor(self, doctor_id: int) -> List[Dict]:
        """Get all completed assignments for a specific doctor"""
        cursor = await self.db.execute("""
            SELECT a.id as assignment_id, a.status, a.timestamp,
                   d.id as doctor_id, d.name as doctor_name, d.category as doctor_category,
                   p.id as patient_id, p.name as patient_name
            FROM assignments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            WHERE a.status = 'completed' AND a.doctor_id = ?
            ORDER BY a.timestamp DESC
        """, (doctor_id,))
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def get_all_assignments(self) -> List[Dict]:
        """Get all assignments with doctor and patient info"""
        cursor = await self.db.execute("""
            SELECT a.id as assignment_id, a.status, a.timestamp,
                   d.id as doctor_id, d.name as doctor_name, d.category as doctor_category,
                   p.id as patient_id, p.name as patient_name
            FROM assignments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            ORDER BY a.timestamp DESC
        """)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    async def update_assignment_status(self, assignment_id: int, status: str):
        """Update assignment status"""
        await self.db.execute(
            "UPDATE assignments SET status = ? WHERE id = ?",
            (status, assignment_id)
        )
        await self.db.commit()
    
    async def delete_assignment(self, assignment_id: int):
        """Delete assignment"""
        await self.db.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
        await self.db.commit()
    
    # Chatbot operations
    async def save_chat_message(self, session_id: str, user_message: str, bot_response: str):
        """Save chatbot conversation"""
        timestamp = datetime.utcnow().isoformat() + "Z"
        await self.db.execute(
            "INSERT INTO chatbot_history (session_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, ?)",
            (session_id, user_message, bot_response, timestamp)
        )
        await self.db.commit()
    
    async def get_chat_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session"""
        cursor = await self.db.execute(
            "SELECT * FROM chatbot_history WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    
    # Helper methods for face/fingerprint matching
    async def find_doctor_by_face(self, face_encoding: List[float]) -> Optional[Dict]:
        """Find doctor by face encoding (requires comparison)"""
        doctors = await self.get_all_doctors()
        from app.services.face_service import FaceRecognitionService
        
        for doctor in doctors:
            if doctor.get('face_embedding'):
                is_match, _ = FaceRecognitionService.compare_faces(
                    doctor['face_embedding'],
                    face_encoding
                )
                if is_match:
                    return doctor
        return None
    
    async def find_doctor_by_fingerprint(self, fingerprint_hash: str) -> Optional[Dict]:
        """Find doctor by fingerprint hash"""
        cursor = await self.db.execute(
            "SELECT * FROM doctors WHERE fingerprint_hash = ?",
            (fingerprint_hash,)
        )
        row = await cursor.fetchone()
        if row:
            doc = dict(row)
            if doc.get('face_embedding'):
                doc['face_embedding'] = json.loads(doc['face_embedding'])
            return doc
        return None
    
    async def find_patient_by_face(self, face_encoding: List[float]) -> Optional[Dict]:
        """Find patient by face encoding (requires comparison)"""
        patients = await self.get_all_patients()
        from app.services.face_service import FaceRecognitionService
        
        for patient in patients:
            if patient.get('face_embedding'):
                is_match, _ = FaceRecognitionService.compare_faces(
                    patient['face_embedding'],
                    face_encoding
                )
                if is_match:
                    return patient
        return None
    
    # Report operations
    async def create_report(self, assignment_id: int, patient_name: str, doctor_name: str,
                           patient_age: str = "", patient_gender: str = "",
                           diagnosis: str = "", symptoms: str = "", 
                           treatment: str = "", medications: str = "", notes: str = "") -> int:
        """Create a new patient report"""
        now = datetime.utcnow().isoformat() + "Z"
        
        cursor = await self.db.execute("""
            INSERT INTO patient_reports 
            (assignment_id, patient_name, patient_age, patient_gender, diagnosis, 
             symptoms, treatment, medications, notes, doctor_name, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (assignment_id, patient_name, patient_age, patient_gender, diagnosis,
              symptoms, treatment, medications, notes, doctor_name, now, now))
        await self.db.commit()
        return cursor.lastrowid
    
    async def get_report_by_assignment(self, assignment_id: int) -> Optional[Dict]:
        """Get report by assignment ID"""
        cursor = await self.db.execute(
            "SELECT * FROM patient_reports WHERE assignment_id = ?", 
            (assignment_id,)
        )
        row = await cursor.fetchone()
        return dict(row) if row else None
    
    async def update_report(self, assignment_id: int, **kwargs) -> None:
        """Update a patient report"""
        # Build update query dynamically
        allowed_fields = ['patient_age', 'patient_gender', 'diagnosis', 'symptoms', 
                         'treatment', 'medications', 'notes']
        updates = []
        values = []
        
        for field in allowed_fields:
            if field in kwargs:
                updates.append(f"{field} = ?")
                values.append(kwargs[field])
        
        if not updates:
            return
        
        # Add updated_at
        updates.append("updated_at = ?")
        values.append(datetime.utcnow().isoformat() + "Z")
        values.append(assignment_id)
        
        query = f"UPDATE patient_reports SET {', '.join(updates)} WHERE assignment_id = ?"
        await self.db.execute(query, values)
        await self.db.commit()


# Global database instance
db = Database()
