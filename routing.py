from sqlalchemy.orm import Session
import models


def resolve_target_city(document_type_code: str, requester: models.Requester) -> str:
    if document_type_code == "casier_judiciaire":
        if not requester.birth_city:
            raise ValueError("This requester has no birth_city on file")
        return requester.birth_city.strip().title()

    elif document_type_code == "minesup_equivalence":
        return "Yaounde"

    elif document_type_code == "minrex_legalis":
        return "Yaounde"

    elif document_type_code == "rccm_extract":
        raise ValueError("RCCM requires a registration_city -- not wired up yet")

    raise ValueError(f"Unknown document_type_code: {document_type_code}")


def find_best_runner(db: Session, target_city: str):
    runners_here = (
        db.query(models.Runner)
        .join(models.RunnerCoverage, models.Runner.id == models.RunnerCoverage.runner_id)
        .filter(models.RunnerCoverage.city.ilike(target_city))
        .all()
    )

    if not runners_here:
        return None

    return runners_here[0]

def log_status_event(db: Session, request_id: int, status: str, note: str = None):
    event = models.StatusEvent(request_id=request_id, status=status, note=note)
    db.add(event)
    db.commit()