from fastapi import FastAPI
from routers import base  

app = FastAPI(
    title="Network Attack Detection API",
    description="API for detecting network attacks using Machine Learning",
    version="1.0.0"
)

app.include_router(base.base_router, tags=["Detection"])