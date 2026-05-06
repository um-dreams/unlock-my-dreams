from fastapi import FastAPI
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Unlock My Dreams API",
    description="Backend API for Unlock My Dreams platform",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to Unlock My Dreams API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

import stripe_routes
import plan_routes

app.include_router(stripe_routes.router, prefix="/stripe", tags=["stripe"])
app.include_router(plan_routes.router, prefix="/api/plans", tags=["plans"])
