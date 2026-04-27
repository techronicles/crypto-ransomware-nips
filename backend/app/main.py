from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.traffic import router as traffic_router
from app.api.routes.blocked_ips import router as blocked_ips_router
from app.api.routes.model_status import router as model_status_router

app = FastAPI(
    title="AI-Driven NIPS API",
    description="Backend API for crypto-ransomware detection and prevention dashboard",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI-Driven NIPS backend is running",
    }


app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(alerts_router, prefix="/api/alerts", tags=["Alerts"])
app.include_router(traffic_router, prefix="/api/traffic", tags=["Traffic"])
app.include_router(blocked_ips_router, prefix="/api/blocked-ips", tags=["Blocked IPs"])
app.include_router(model_status_router, prefix="/api/model", tags=["Model"])