from app.db.session import SessionLocal

from app.rfps.models import RFPRequirement

from app.rfp_requirements.repository import (
    RFPRequirementRepository,
)


if __name__ == "__main__":

    db = SessionLocal()

    try:

        repository = (
            RFPRequirementRepository(db)
        )

        requirement = RFPRequirement(
            rfp_id=1,
            title=(
                "Enterprise Document Management "
                "and AI Assistant Platform"
            ),
            client=(
                "Acme Financial Services Pvt. Ltd."
            ),
            submission_deadline=(
                "30 August 2026, 5:00 PM IST"
            ),
            project_overview=(
                "Enterprise Document Management "
                "and AI Assistant Platform."
            ),
            mandatory_requirements=[
                "The proposed solution must provide authenticated user access.",
                "The platform must support role-based authorization.",
            ],
            technical_requirements=[
                "The platform should expose RESTful APIs.",
                "The solution should support PostgreSQL.",
            ],
            functional_requirements=[
                "Users must be able to upload documents.",
                "Users must be able to search documents.",
            ],
            deliverables=[
                "Production-ready web application.",
                "Technical documentation.",
            ],
            evaluation_criteria=[
                "Technical solution and architecture – 30%",
                "Commercial proposal – 10%",
            ],
            commercial_requirements=[
                "The commercial proposal must clearly identify implementation costs.",
            ],
            eligibility_requirements=[
                "The bidder must be a legally registered business entity.",
            ],
        )

        created = repository.create(
            requirement
        )

        print(
            "Requirement ID:",
            created.id,
        )

        print(
            "RFP ID:",
            created.rfp_id,
        )

        print(
            "Title:",
            created.title,
        )

        print(
            "Client:",
            created.client,
        )

    finally:

        db.close()