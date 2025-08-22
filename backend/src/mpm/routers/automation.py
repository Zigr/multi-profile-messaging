# backend/routers/automation.py
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from mpm.database import SessionLocal
import mpm.models as models
from mpm.connectors.playwright_automation import PlaywrightAutomation

router = APIRouter(prefix="/automation", tags=["automation"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CaptureReq(BaseModel):
    profile_id: int
    login_url: str
    max_wait_ms: int = 120_000
    headless: bool = False


class RefreshReq(BaseModel):
    profile_id: int
    headless: bool = True


class CookieResp(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    cookies: list
    user_agent: str | None = None
    storage_state_path: str | None = None


@router.post("/cookies/capture", response_model=CookieResp)
def capture_cookies(req: CaptureReq, db: Session = Depends(get_db)):
    prof = db.query(models.Profile).get(req.profile_id)
    if not prof:
        raise HTTPException(404, "Profile not found")
    if prof.platform == "email":
        raise HTTPException(400, "Cookie capture not applicable for email profiles")

    proxy = prof.proxy
    pwa = PlaywrightAutomation(headless=req.headless)
    res = pwa.capture_cookies(
        login_url=req.login_url,
        max_wait_ms=req.max_wait_ms,
        proxy=proxy,
        storage_state_dir="./storage_states",
        storage_state_name=f"profile_{prof.id}.json",
    )

    # persist to profile.credentials
    creds = dict(prof.credentials or {})
    creds["cookies"] = res["cookies"]
    creds["storage_state_path"] = res["storage_state_path"]
    creds["user_agent"] = res.get("user_agent")
    prof.credentials = creds
    db.add(prof)
    db.commit()
    db.refresh(prof)

    return CookieResp(**res)


@router.get("/cookies/{profile_id}", response_model=CookieResp)
def get_cookies(profile_id: int, db: Session = Depends(get_db)):
    prof = db.query(models.Profile).get(profile_id)
    if not prof:
        raise HTTPException(404, "Profile not found")
    creds = prof.credentials or {}
    return CookieResp(
        cookies=creds.get("cookies", []),
        user_agent=creds.get("user_agent"),
        storage_state_path=creds.get("storage_state_path"),
    )


@router.post("/cookies/refresh", response_model=CookieResp)
def refresh_cookies(req: RefreshReq, db: Session = Depends(get_db)):
    prof = db.query(models.Profile).get(req.profile_id)
    if not prof:
        raise HTTPException(404, "Profile not found")

    storage_path = (prof.credentials or {}).get("storage_state_path")
    if not storage_path:
        raise HTTPException(
            400, "No storage_state_path on this profile. Capture first."
        )

    proxy = prof.proxy
    pwa = PlaywrightAutomation(headless=req.headless)
    res = pwa.load_storage_state(storage_state_path=storage_path, proxy=proxy)

    # Update cookies snapshot
    creds = dict(prof.credentials or {})
    creds["cookies"] = res["cookies"]
    creds["user_agent"] = res.get("user_agent")
    prof.credentials = creds
    db.add(prof)
    db.commit()
    db.refresh(prof)

    return CookieResp(**res)
