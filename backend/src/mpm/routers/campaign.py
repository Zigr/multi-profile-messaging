from fastapi import APIRouter, HTTPException
from mpm.database import SessionLocal
from mpm.models import Profile

# You’ll wire these functions into your Celery tasks:
from tasks import start_campaign_task, stop_campaign_task

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.post("/{profile_id}/start")
def start_campaign(profile_id: int):
    db = SessionLocal()
    profile = db.query(Profile).get(profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")
    # Enqueue Celery task
    start_campaign_task.delay(profile_id)
    return {"status": "queued", "action": "start"}


@router.post("/{profile_id}/stop")
def stop_campaign(profile_id: int):
    # Implementation depends on how you track tasks—this is a stub
    stop_campaign_task.delay(profile_id)
    return {"status": "queued", "action": "stop"}
