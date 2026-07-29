from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import routing

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DokiSure")


@app.get("/")
def read_root():
    return {"message": "DokiSure is running"}


@app.post("/requesters")
def create_requester(phone: str, full_name: str, birth_city: str = None, db: Session = Depends(get_db)):
    new_requester = models.Requester(phone=phone, full_name=full_name, birth_city=birth_city)
    db.add(new_requester)
    db.commit()
    db.refresh(new_requester)
    return new_requester


@app.post("/runners")
def create_runner(phone: str, full_name: str, base_city: str, db: Session = Depends(get_db)):
    new_runner = models.Runner(phone=phone, full_name=full_name, base_city=base_city)
    db.add(new_runner)
    db.commit()
    db.refresh(new_runner)
    return new_runner


@app.get("/document-types")
def list_document_types(db: Session = Depends(get_db)):
    return db.query(models.DocumentType).all()

@app.post("/runners/{runner_id}/coverage")
def add_coverage(runner_id: int, city: str, db: Session = Depends(get_db)):
    coverage = models.RunnerCoverage(runner_id=runner_id, city=city)
    db.add(coverage)
    db.commit()
    return {"runner_id": runner_id, "city": city, "added": True}

@app.post("/requests")
def create_request(requester_id: int, document_type_code: str, db: Session = Depends(get_db)):
    new_request = models.RequestRecord(
        requester_id=requester_id,
        document_type_code=document_type_code,
        status="submitted"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@app.post("/requests/{request_id}/assign")
def assign_runner(request_id: int, db: Session = Depends(get_db)):
    request = db.query(models.RequestRecord).filter(models.RequestRecord.id == request_id).first()
    if not request:
        return {"error": "request not found"}

    requester = db.query(models.Requester).filter(models.Requester.id == request.requester_id).first()
    if not requester:
        return {"error": "requester not found"}

    try:
        target_city = routing.resolve_target_city(request.document_type_code, requester)
    except ValueError as e:
        return {"error": str(e)}

    best_runner = routing.find_best_runner(db, target_city)

    request.target_city = target_city

    if best_runner:
        request.runner_id = best_runner.id
        request.status = "runner_assigned"
        db.commit()
        routing.log_status_event(db, request.id, "runner_assigned", f"Assigned to {best_runner.full_name} in {target_city}")
    else:
        request.status = "awaiting_runner"
        db.commit()
        routing.log_status_event(db, request.id, "awaiting_runner", f"No runner available in {target_city}")

    db.refresh(request)
    return request

@app.get("/requests/{request_id}/history")
def get_request_history(request_id: int, db: Session = Depends(get_db)):
    return db.query(models.StatusEvent).filter(models.StatusEvent.request_id == request_id).all()