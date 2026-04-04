from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database_sqlite import db
from app.routes import registration, patient, verification, dashboard, admin, chatbot, reports
from app.backup import start_backup_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    await db.connect()
    print("Hospital Safety Checker API Started")
    
    # Start MySQL Backup Schedule
    start_backup_scheduler()
    
    yield
    # Shutdown
    await db.close()
    print("Hospital Safety Checker API Stopped")

# Create FastAPI app
app = FastAPI(
    title="Hospital Safety Checker API",
    description="Biometric-based hospital safety and patient management system",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(registration.router)
app.include_router(patient.router)
app.include_router(verification.router)
app.include_router(dashboard.router)
app.include_router(admin.router)
app.include_router(chatbot.router)
app.include_router(reports.router)

@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Hospital Safety Checker API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "registration": "/api/registration",
            "patient": "/api/patient",
            "verification": "/api/verification",
            "dashboard": "/api/dashboard",
            "admin": "/api/admin",
            "chatbot": "/api/chatbot",
            "reports": "/api/reports"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "database": "connected" if db.db else "disconnected"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
