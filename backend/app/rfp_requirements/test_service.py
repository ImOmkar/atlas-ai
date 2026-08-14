
from app.db.session import SessionLocal

from app.rfp_requirements.service import (
    RFPRequirementService,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        service = (
            RFPRequirementService(db)
        )

        requirement = (
            service.get_for_rfp(
                project_id=1,
                rfp_id=5,
            )
        )

        print(
            "Title:",
            requirement.title,
        )

        print(
            "Client:",
            requirement.client,
        )

        print(
            "Deadline:",
            requirement.submission_deadline,
        )

        print(
            "\nMandatory Requirements:"
        )

        for item in (
            requirement.mandatory_requirements
        ):

            print(
                "-",
                item,
            )

        print(
            "\nTechnical Requirements:"
        )

        for item in (
            requirement.technical_requirements
        ):

            print(
                "-",
                item,
            )

    finally:

        db.close()