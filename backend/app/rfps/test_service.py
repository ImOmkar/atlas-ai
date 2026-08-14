# from app.db.session import SessionLocal

# from app.rfps.service import RFPService


# if __name__ == "__main__":

#     db = SessionLocal()

#     try:

#         service = RFPService(db)

#         rfp = service.create_from_document(
#             project_id=1,
#             document_id=20,
#         )

#         print(
#             "RFP ID:",
#             rfp.id,
#         )

#         print(
#             "Project ID:",
#             rfp.project_id,
#         )

#         print(
#             "Document ID:",
#             rfp.document_id,
#         )

#         print(
#             "Status:",
#             rfp.status,
#         )

#     finally:

#         db.close()


from sqlalchemy.orm import configure_mappers

from app.db.session import SessionLocal
from app.db.base import Base
import app.db.models
from app.rfps.service import RFPService


if __name__ == "__main__":

    configure_mappers()

    db = SessionLocal()

    try:

        service = RFPService(db)

        rfp = service.create_from_document(
            project_id=1,
            document_id=20,
        )

        print("RFP ID:", rfp.id)
        print("Project ID:", rfp.project_id)
        print("Document ID:", rfp.document_id)
        print("Status:", rfp.status)

    finally:
        db.close()