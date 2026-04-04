"""
MongoDB Data Viewer
Simple script to view all data in the Hospital Safety Checker database
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

async def view_database():
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["hospital_safety_checker"]
    
    print("=" * 80)
    print("HOSPITAL SAFETY CHECKER - DATABASE VIEWER")
    print("=" * 80)
    print()
    
    # View Doctors
    print("📋 DOCTORS")
    print("-" * 80)
    doctors = await db.doctors.find().to_list(length=None)
    if doctors:
        for i, doc in enumerate(doctors, 1):
            print(f"\n{i}. Doctor ID: {doc['_id']}")
            print(f"   Name: {doc.get('name', 'N/A')}")
            print(f"   Category: {doc.get('category', 'N/A')}")
            print(f"   Has Face: {'Yes' if doc.get('face_embedding') else 'No'}")
            print(f"   Has Fingerprint: {'Yes' if doc.get('fingerprint_hash') else 'No'}")
            print(f"   Created: {doc.get('created_at', 'N/A')}")
    else:
        print("   No doctors found")
    
    print("\n" + "=" * 80)
    
    # View Patients
    print("\n📋 PATIENTS")
    print("-" * 80)
    patients = await db.patients.find().to_list(length=None)
    if patients:
        for i, patient in enumerate(patients, 1):
            print(f"\n{i}. Patient ID: {patient['_id']}")
            print(f"   Name: {patient.get('name', 'N/A')}")
            print(f"   Has Face: {'Yes' if patient.get('face_embedding') else 'No'}")
            print(f"   Created: {patient.get('created_at', 'N/A')}")
    else:
        print("   No patients found")
    
    print("\n" + "=" * 80)
    
    # View Assignments
    print("\n📋 ASSIGNMENTS")
    print("-" * 80)
    assignments = await db.assignments.find().to_list(length=None)
    if assignments:
        for i, assignment in enumerate(assignments, 1):
            print(f"\n{i}. Assignment ID: {assignment['_id']}")
            print(f"   Doctor ID: {assignment.get('doctor_id', 'N/A')}")
            print(f"   Patient ID: {assignment.get('patient_id', 'N/A')}")
            print(f"   Status: {assignment.get('status', 'N/A')}")
            print(f"   Timestamp: {assignment.get('timestamp', 'N/A')}")
    else:
        print("   No assignments found")
    
    print("\n" + "=" * 80)
    
    # Statistics
    print("\n📊 STATISTICS")
    print("-" * 80)
    print(f"Total Doctors: {len(doctors)}")
    print(f"Total Patients: {len(patients)}")
    print(f"Total Assignments: {len(assignments)}")
    waiting = sum(1 for a in assignments if a.get('status') == 'waiting')
    completed = sum(1 for a in assignments if a.get('status') == 'completed')
    print(f"Waiting: {waiting}")
    print(f"Completed: {completed}")
    
    print("\n" + "=" * 80)
    print()
    
    client.close()

if __name__ == "__main__":
    print("\nConnecting to MongoDB...")
    try:
        asyncio.run(view_database())
        print("\n✅ Database view complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure MongoDB is running on mongodb://localhost:27017")
