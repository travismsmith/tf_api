from app.server.routers import plan, apply
from fastapi import FastAPI

app = FastAPI(title="Terraform API", version="0.0.2")

app.include_router(plan.router)
app.include_router(apply.router)
