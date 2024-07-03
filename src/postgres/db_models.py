from uuid import uuid4
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy import (
    String,
    DateTime,
    Boolean
)


class Base(DeclarativeBase):
    pass

class Vectorstore(Base):
    __tablename__ = "vectorstore"
    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    company_name = mapped_column(String)
    content = mapped_column(String) 
    embedding = mapped_column(Vector(1536))
    is_deleted = mapped_column(Boolean, nullable=False, default=False)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, onupdate=func.now())


class ChatMessages(Base):
    __tablename__ = 'chat_messages'

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    chat_id = mapped_column(String, unique=False, nullable=False)
    role = mapped_column(String(10), unique=False, nullable=False)
    content = mapped_column(String, unique=False, nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, onupdate=func.now())
        