from database import SessionLocal
import models

db = SessionLocal()

document_types = [
    models.DocumentType(code="casier_judiciaire", name="Casier judiciaire", government_fee=2100, runner_fee=2500, platform_margin=1400, routing_rule="birth_city"),
    models.DocumentType(code="minrex_legalis", name="Legalisation MINREX", government_fee=20000, runner_fee=4500, platform_margin=2500, routing_rule="yaounde_douala"),
    models.DocumentType(code="minesup_equivalence", name="Equivalence diplome MINESUP", government_fee=25000, runner_fee=5000, platform_margin=2000, routing_rule="yaounde"),
    models.DocumentType(code="rccm_extract", name="Extrait RCCM", government_fee=3000, runner_fee=3000, platform_margin=2000, routing_rule="registration_city"),
]

for doc_type in document_types:
    db.merge(doc_type)  # merge = insert or update, safe to run multiple times

db.commit()
db.close()
print("Document types seeded.")