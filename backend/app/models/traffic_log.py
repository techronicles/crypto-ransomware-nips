from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base


class TrafficLog(Base):
    __tablename__ = "traffic_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source_ip = Column(String, nullable=False)
    destination_ip = Column(String, nullable=False)
    protocol = Column(String, nullable=False)
    packet_size = Column(Integer, nullable=False)
    prediction = Column(String, default="Benign")