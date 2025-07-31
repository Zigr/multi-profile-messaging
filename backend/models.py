from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    ForeignKey,
    JSON,
)
from sqlalchemy.sql import func
from database import Base
import enum


class PlatformEnum(str, enum.Enum):
    telegram = "telegram"
    email = "email"


class ListTypeEnum(str, enum.Enum):
    whitelist = "whitelist"
    blacklist = "blacklist"


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    platform = Column(Enum(PlatformEnum), nullable=False)
    credentials = Column(JSON, nullable=False)  # tokens, cookies, SMTP creds, etc.
    proxy = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Template(Base):
    __tablename__ = "templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    subject = Column(String, nullable=True)  # for email
    body = Column(Text, nullable=False)  # message text with variables
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ListEntry(Base):
    __tablename__ = "list_entries"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    type = Column(Enum(ListTypeEnum), nullable=False)
    value = Column(String, nullable=False)  # e.g. user id, email address


class LogEntry(Base):
    __tablename__ = "log_entries"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    action = Column(String, nullable=False)  # e.g. "send_message", "invite", etc.
    status = Column(String, nullable=False)  # "success" / "error"
    detail = Column(Text, nullable=True)  # error message or extra info
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
