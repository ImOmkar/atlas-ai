
from app.rest.models import (
    APIRequest,
)


class RESTValidator:

    ALLOWED_METHODS = {
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }

    def validate(
        self,
        request: APIRequest,
    ):

        if request.method not in self.ALLOWED_METHODS:

            raise ValueError(
                "Unsupported HTTP method."
            )

        if not request.path.startswith("/"):

            raise ValueError(
                "Invalid API path."
            )

        return True

    

# if __name__ == "__main__":

#     from app.rest.models import APIRequest

#     validator = RESTValidator()

#     request = APIRequest(
#         method="GET",
#         path="/employees/101",
#         body=None,
#     )

#     print(
#         validator.validate(
#             request,
#         )
#     )