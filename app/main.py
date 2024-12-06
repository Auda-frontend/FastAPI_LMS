# main.py
from fastapi import FastAPI
from app.endpoints.admin import router as admin_router
from app.endpoints.analytics import router as analytics_router
from app.endpoints.special_endpoints import router as special_endpoints_router
from app.endpoints.student import router as student_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Library Management System!"}
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(special_endpoints_router, prefix="/special", tags=["Special Endpoints"])
app.include_router(student_router, prefix="/students", tags=["Students"])
