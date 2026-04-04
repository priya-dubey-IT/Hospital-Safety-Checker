import os
import sqlite3
import pymysql
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

# MySQL configuration from environment variables (with fallbacks)
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "hospital_safety_backup")

def sync_sqlite_to_mysql():
    """
    Reads from the local SQLite hospital_safety.db and syncs everything to the MySQL backup database.
    This process completely replaces the MySQL data with the live SQLite data.
    Runs every midnight.
    """
    print(f"\n[{datetime.now()}] Starting daily MySQL backup...")
    try:
        # Create MySQL connection
        mysql_conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        mysql_cursor = mysql_conn.cursor()
        
        # Create backup database if it doesn't exist yet
        mysql_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
        mysql_conn.select_db(MYSQL_DATABASE)
        
        # Connect to SQLite to read active data
        sqlite_conn = sqlite3.connect("hospital_safety.db")
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Target tables to back up in order (for foreign keys if needed, though we truncate)
        tables = ["doctors", "patients", "assignments", "chatbot_history", "patient_reports"]
        
        for table in tables:
            # Get SQLite schema
            sqlite_cursor.execute(f"PRAGMA table_info({table})")
            columns = sqlite_cursor.fetchall()
            
            if not columns:
                continue
                
            # Translate SQLite column schema to MySQL
            cols_def = []
            for col in columns:
                col_name = col['name']
                col_type = col['type']
                
                # Simplistic type casting from SQLite -> MySQL
                if "INT" in col_type.upper():
                    mysql_type = "INT"
                elif "TEXT" in col_type.upper():
                    mysql_type = "LONGTEXT"
                else:
                    mysql_type = "VARCHAR(255)"
                
                if col_name.lower() == "id":
                    cols_def.append(f"{col_name} INT PRIMARY KEY AUTO_INCREMENT")
                else:
                    cols_def.append(f"{col_name} {mysql_type}")
            
            # Create matching tables in MySQL
            mysql_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(cols_def)})")
            
            # Clear existing backup data in this table
            mysql_cursor.execute(f"SET FOREIGN_KEY_CHECKS=0;")
            mysql_cursor.execute(f"TRUNCATE TABLE {table}")
            mysql_cursor.execute(f"SET FOREIGN_KEY_CHECKS=1;")
            
            # Fetch all rows from SQLite
            sqlite_cursor.execute(f"SELECT * FROM {table}")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                insert_query = f"INSERT INTO {table} ({', '.join([c['name'] for c in columns])}) VALUES ({', '.join(['%s'] * len(columns))})"
                
                # Convert sqlite3.Row objects to standard tuples
                values = [tuple(row) for row in rows]
                mysql_cursor.executemany(insert_query, values)
                
        # Commit MySQL transaction
        mysql_conn.commit()
        
        # Close connections cleanly
        sqlite_conn.close()
        mysql_conn.close()
        
        print(f"Daily MySQL backup completed successfully at {datetime.now()}\n")
        
    except Exception as e:
        print(f"Error during MySQL backup: {e}\n")

# Global APScheduler instance
scheduler = AsyncIOScheduler()

def start_backup_scheduler():
    """Initializes and starts the background scheduler for MySQL backups."""
    # Skip scheduler in testing environments to avoid event loop conflicts
    if os.getenv("PYTEST_CURRENT_TEST"):
        return

    if scheduler.running:
        return

    scheduler.add_job(
        sync_sqlite_to_mysql,
        CronTrigger(hour=0, minute=0),  # Runs strictly at Midnight (00:00)
        id="mysql_daily_backup",
        name="Daily MySQL Database Backup",
        replace_existing=True
    )
    try:
        scheduler.start()
        print("MySQL Backup Scheduler started - Backup scheduled for midnight (00:00) daily.")
    except (RuntimeError, Exception) as e:
        print(f"Could not start backup scheduler: {e}")
