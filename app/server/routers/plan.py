import app.clients.tfapi as tf
from app.clients.logger import logger
from fastapi import APIRouter, UploadFile

router = APIRouter()


@router.post("/plan")
async def tf_plan(file: UploadFile):
    tfc = tf.client("DEV", "test")
    cv = tfc.create_cv(file)
    tfc.create_run(cv)
    return {"filename": file.filename}