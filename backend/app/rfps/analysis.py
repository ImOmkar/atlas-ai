
import re

from app.rfp_requirements.service import (
    RFPRequirementService,
)


class RFPAnalysisService:

    def __init__(self, db):

        self.requirement_service = (
            RFPRequirementService(db)
        )

    def analyze(
        self,
        project_id: int,
        rfp_id: int,
    ):

        requirement = (
            self.requirement_service.get_for_rfp(
                project_id=project_id,
                rfp_id=rfp_id,
            )
        )

        evaluation_criteria = []

        for item in (
            requirement.evaluation_criteria
        ):

            match = re.search(
                r"(.+?)\s*[–-]\s*(\d+(?:\.\d+)?%)",
                item,
            )

            if match:

                evaluation_criteria.append(
                    {
                        "criterion": (
                            match.group(1).strip()
                        ),
                        "weightage": (
                            match.group(2)
                        ),
                    }
                )

            else:

                evaluation_criteria.append(
                    {
                        "criterion": item,
                        "weightage": "",
                    }
                )

        return {
            "rfp_id": rfp_id,

            "title": requirement.title,

            "client": requirement.client,

            "submission_deadline": (
                requirement.submission_deadline
            ),

            "summary": {
                "mandatory_requirements_count": len(
                    requirement.mandatory_requirements
                ),

                "technical_requirements_count": len(
                    requirement.technical_requirements
                ),

                "functional_requirements_count": len(
                    requirement.functional_requirements
                ),

                "deliverables_count": len(
                    requirement.deliverables
                ),

                "evaluation_criteria_count": len(
                    requirement.evaluation_criteria
                ),

                "commercial_requirements_count": len(
                    requirement.commercial_requirements
                ),

                "eligibility_requirements_count": len(
                    requirement.eligibility_requirements
                ),
            },

            "evaluation_criteria": (
                evaluation_criteria
            ),
        }