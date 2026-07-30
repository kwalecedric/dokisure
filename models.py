from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base


class Requester(Base):
    __tablename__ = "requesters"

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    birth_city = Column(String, nullable=True)


class Runner(Base):
    __tablename__ = "runners"

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    base_city = Column(String, nullable=False)
class DocumentType(Base):
    __tablename__ = "document_types"

    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    government_fee = Column(Integer, nullable=False)
    runner_fee = Column(Integer, nullable=False)
    platform_margin = Column(Integer, nullable=False)
    routing_rule = Column(String, nullable=False)

class RunnerCoverage(Base):
    __tablename__ = "runner_coverage"

    runner_id = Column(Integer, primary_key=True)
    city = Column(String, primary_key=True)

class RequestRecord(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, nullable=False)
    document_type_code = Column(String, nullable=False)
    target_city = Column(String, nullable=True)
    runner_id = Column(Integer, nullable=True)
    status = Column(String, default="submitted")

class StatusEvent(Base):
    __tablename__ = "status_events"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    provider = Column(String, nullable=True)
    transaction_ref = Column(String, nullable=True)
    escrow_status = Column(String, default="held")