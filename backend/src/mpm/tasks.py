import os
import random
from celery import Celery
from celery.utils.log import get_task_logger
from sqlalchemy.orm import Session
from database import SessionLocal
from connectors.smtp_connector import SMTPConnector
from connectors.playwright_auth import PlaywrightAuth
from jinja2 import Template as JinjaTemplate
from models import Profile, Template as TemplateModel, LogEntry

# 1) Configure Celery broker (Redis):
celery = Celery(
    "mpm_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
)
# Optional: default rate (you can also set per-task)
celery.conf.task_default_rate_limit = "1/s"

logger = get_task_logger(__name__)


# 2) Helper to render Jinja2 templates
class Renderer:
    def render(self, template_str: str, vars: dict) -> str:
        return JinjaTemplate(template_str).render(**vars)


# 3) Core send task, rate-limited per profile (~1 msg/3.6s to hit 1 000/hr)
@celery.task(bind=True, rate_limit="1/3.6s")
def send_message_task(
    self, profile_id: int, template_id: int, recipient: str, context_vars: dict
):
    db: Session = SessionLocal()
    try:
        # Load profile & template
        profile = db.query(Profile).get(profile_id)
        if profile is None:
            raise ValueError(f"Profile with id {profile_id} not found")
        tmpl = db.query(TemplateModel).get(template_id)
        if not isinstance(tmpl, TemplateModel):
            raise ValueError(f"Template with id {template_id} not found")
        if tmpl is None:
            raise ValueError(f"Template with id {template_id} not found")

        # Render body (and subject for email)
        renderer = Renderer()
        body = renderer.render(str(tmpl.body), context_vars)
        subject = renderer.render(str(tmpl.subject or ""), context_vars)

        # Dispatch via the right connector
        if profile.platform == "email":
            creds = profile.credentials or {}
            smtp = SMTPConnector(
                host=creds.get("host", ""),
                port=int(creds.get("port", 0)),
                user=creds.get("user"),
                password=creds.get("password"),
                use_ssl=not creds.get("use_mailcatcher", False),
                use_mailcatcher=creds.get("use_mailcatcher", False),
            )
            smtp.send_email(recipient, subject, body)
            action = "send_message_email"
        else:
            # Placeholder for Telegram connector logic
            action = "send_message_telegram"
            # TODO: integrate your Telegram connector here

        # Log success
        log = LogEntry(
            profile_id=profile_id,
            action=action,
            status="success",
            detail=None,
        )
        db.add(log)
        db.commit()

    except Exception as e:
        # Log failure
        logger.error("send_message_task failed: %s", e)
        log = LogEntry(
            profile_id=profile_id,
            action="send_message",
            status="error",
            detail=str(e),
        )
        db.add(log)
        db.commit()

    finally:
        db.close()


# 4) Campaign control tasks
@celery.task
def start_campaign_task(
    profile_id: int,
    template_id: int,
    recipients: list,
    vars_list: list,
    min_delay: float = 1.0,
    max_delay: float = 5.0,
):
    """
    Enqueue send_message_task for each recipient with a random delay.
    `recipients` is a list of recipient identifiers (emails or user IDs).
    `vars_list` is a parallel list of dicts for template rendering.
    """
    for recipient, ctx in zip(recipients, vars_list):
        delay = random.uniform(min_delay, max_delay)
        send_message_task.apply_async(
            args=[profile_id, template_id, recipient, ctx],
            countdown=delay,
        )


@celery.task
def stop_campaign_task(profile_id: int):
    """
    Signal to stop an in-progress campaign.
    You’ll need to implement a check in send_message_task (e.g. via a DB flag)
    to actually halt further sends.
    """
    # TODO: flip a “campaign_active” flag in the Profile or Campaign table
    pass
