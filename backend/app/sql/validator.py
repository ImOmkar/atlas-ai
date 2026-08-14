import re


class SQLValidator:

    FORBIDDEN = [

        "INSERT",

        "UPDATE",

        "DELETE",

        "DROP",

        "ALTER",

        "TRUNCATE",

        "CREATE",

        "GRANT",

        "REVOKE",

        "EXEC",

        "EXECUTE",

        "CALL",

    ]

    def validate(
        self,
        query: str,
    ):

        sql = query.upper()

        for keyword in self.FORBIDDEN:

            if re.search(
                rf"\b{keyword}\b",
                sql,
            ):

                raise ValueError(
                    f"Forbidden SQL: {keyword}"
                )

        return True




# if __name__ == "__main__":

#     validator = SQLValidator()

#     validator.validate(
#         "UPDATE documents SET id=1;"
#     )

#     print("Valid")