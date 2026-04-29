from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    threat_type = Column(String, nullable=False)
    severity = Column(String, default="Medium")
    status = Column(String, default="Monitoring")