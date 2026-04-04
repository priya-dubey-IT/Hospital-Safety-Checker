"""
Simple SQLite Database Viewer
View all data in the Hospital Safety Checker database
"""

import sqlite3
import json
from datetime import datetime

def view_database():
    # Connect to database
    conn = sqlite3.connect('hospital_safety.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    print("=" * 80)
    print("HOSPITAL SAFETY CHECKER - DATABASE VIEWER")
    print("=" * 80)
    print()
    
    # View Doctors
    print("📋 DOCTORS")
    print("-" * 80)
    cursor.execute("SELECT * FROM doctors ORDER BY created_at DESC")
    doctors = cursor.fetchall()
    if doctors:
        for i, doc in enumerate(doctors, 1):
            print(f"\n{i}. Doctor ID: {doc['id']}")
            print(f"   Name: {doc['name']}")
            print(f"   Category: {doc['category']}")
            print(f"   Has Face: {'Yes' if doc['face_embedding'] else 'No'}")
            print(f"   Has Fingerprint: {'Yes' if doc['fingerprint_hash'] else 'No'}")
            print(f"   Created: {doc['created_at']}")
    else:
        print("   No doctors found")
    
    print("\n" + "=" * 80)
    
    # View Patients
    print("\n📋 PATIENTS")
    print("-" * 80)
    cursor.execute("SELECT * FROM patients ORDER BY created_at DESC")
    patients = cursor.fetchall()
    if patients:
        for i, patient in enumerate(patients, 1):
            print(f"\n{i}. Patient ID: {patient['id']}")
            print(f"   Name: {patient['name']}")
            print(f"   Has Face: {'Yes' if patient['face_embedding'] else 'No'}")
            print(f"   Created: {patient['created_at']}")
    else:
        print("   No patients found")
    
    print("\n" + "=" * 80)
    
    # View Assignments
    print("\n📋 ASSIGNMENTS")
    print("-" * 80)
    cursor.execute("""
        SELECT a.id as assignment_id, a.status, a.timestamp,
               d.name as doctor_name, p.name as patient_name
        FROM assignments a
        JOIN doctors d ON a.doctor_id = d.id
        JOIN patients p ON a.patient_id = p.id
        ORDER BY a.timestamp DESC
    """)
    assignments = cursor.fetchall()
    if assignments:
        for i, assignment in enumerate(assignments, 1):
            print(f"\n{i}. Assignment ID: {assignment['assignment_id']}")
            print(f"   Doctor: {assignment['doctor_name']}")
            print(f"   Patient: {assignment['patient_name']}")
            print(f"   Status: {assignment['status']}")
            print(f"   Timestamp: {assignment['timestamp']}")
    else:
        print("   No assignments found")
    
    print("\n" + "=" * 80)
    
    # Statistics
    print("\n📊 STATISTICS")
    print("-" * 80)
    print(f"Total Doctors: {len(doctors)}")
    print(f"Total Patients: {len(patients)}")
    print(f"Total Assignments: {len(assignments)}")
    
    cursor.execute("SELECT COUNT(*) as count FROM assignments WHERE status = 'waiting'")
    waiting = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM assignments WHERE status = 'completed'")
    completed = cursor.fetchone()['count']
    
    print(f"Waiting: {waiting}")
    print(f"Completed: {completed}")
    
    print("\n" + "=" * 80)
    print()
    
    conn.close()

if __name__ == "__main__":
    try:
        view_database()
        print("\n✅ Database view complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you're in the backend directory and hospital_safety.db exists")
