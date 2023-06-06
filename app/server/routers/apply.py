import app.clients.tfapi as tf
from fastapi import APIRouter, UploadFile
from app.clients.logger import logger
import time

router = APIRouter()

@router.post("/apply")
async def tf_plan(file: UploadFile):
    complete_status = [
        "planned",
        "planned_and_finished",
        "applied",
        "discarded",
        "errored",
        "canceled",
        "force_canceled",
    ]
    apply = ""
    apply_output = ""
    tfc = tf.client("DEV", "test")
    cv = tfc.create_cv(file)
    run = tfc.create_run(cv, False)
    while run["data"]["attributes"]["status"] not in complete_status:
        run = tfc.get_run(run["data"]["id"])
        logger.debug(run["data"]["attributes"]["status"])
        time.sleep(5)
    plan = tfc.get_plan(run['data']['relationships']['plan']['data']['id'])
    plan_output = tfc.get_plan_output(run["data"]["id"])
    if run["data"]["attributes"]["status"] == 'planned':
        tfc.apply_run(run["data"]["id"])
        run = tfc.get_run(run["data"]["id"])
        while run["data"]["attributes"]["status"] not in complete_status:
            run = tfc.get_run(run["data"]["id"])
            logger.debug(run["data"]["attributes"]["status"])
            time.sleep(5)
        apply = tfc.get_apply(run['data']['relationships']['apply']['data']['id'])
        apply_output = tfc.get_plan_output(run["data"]["id"])
    return {"filename": file.filename, "run": run, "plan_output": plan_output, "plan": plan, "apply_output": apply_output, "apply": apply}
