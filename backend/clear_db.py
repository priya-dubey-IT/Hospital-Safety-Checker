"""
Clear all data from the Hospital Safety Checker database
"""

import sqlite3

def clear_database():
    conn = sqlite3.connect('hospital_safety.db')
    cursor = conn.cursor()
    
    print("🗑️  Clearing all data from database...")
    
    # Delete all records
    cursor.execute("DELETE FROM assignments")
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM doctors")
    cursor.execute("DELETE FROM chatbot_history")
    
    # Reset ID counters
    cursor.execute("DELETE FROM sqlite_sequence")
    
    conn.commit()
    
    # Show counts
    cursor.execute("SELECT COUNT(*) FROM doctors")
    doctors = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM patients")
    patients = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM assignments")
    assignments = cursor.fetchone()[0]
    
    print(f"✅ Database cleared!")
    print(f"   Doctors: {doctors}")
    print(f"   Patients: {patients}")
    print(f"   Assignments: {assignments}")
    
    conn.close()

if __name__ == "__main__":
    response = input("Are you sure you want to clear ALL data? (yes/no): ")
    if response.lower() == 'yes':
        clear_database()
    else:
        print("❌ Cancelled")
