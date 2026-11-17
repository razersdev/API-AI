
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from database.connection import Base


class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(Text, nullable=False)

    category = Column(
        String(50),
        nullable=False,
        index=True,
    )

    source_conversation_id = Column(
        String(100),
        nullable=True,
    )

    importance = Column(
        Integer,
        default=1,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
