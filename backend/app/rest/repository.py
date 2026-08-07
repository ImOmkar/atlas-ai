
import requests

from app.rest.models import APIRequest


class RESTRepository:

    def execute(
        self,
        base_url: str,
        request: APIRequest,
        headers: dict | None = None,
    ):

        response = requests.request(
            method=request.method,
            url=f"{base_url}{request.path}",
            json=request.body,
            headers=headers or {},
        )

        response.raise_for_status()

        return response.json()


    

# if __name__ == "__main__":

#     from app.rest.models import APIRequest

#     repository = RESTRepository()

#     request = APIRequest(
#         method="GET",
#         path="/users/1",
#         body=None,
#     )

#     result = repository.execute(
#         base_url="https://jsonplaceholder.typicode.com",
#         request=request,
#     )

#     print(result)