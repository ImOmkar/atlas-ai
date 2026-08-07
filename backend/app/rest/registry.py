

class RESTRegistry:

    def __init__(self):

        self.systems = {

            "jsonplaceholder": {

                "base_url":
                    "https://jsonplaceholder.typicode.com",

                "api_spec": """
GET /users
GET /users/{id}
POST /users
""",

                "headers": {},
            }

        }

    def get(
        self,
        system: str,
    ):

        if system not in self.systems:

            raise ValueError(
                "Unknown REST system."
            )

        return self.systems[system]

    


# if __name__ == "__main__":

#     registry = RESTRegistry()

#     print(
#         registry.get(
#             "jsonplaceholder",
#         )
#     )