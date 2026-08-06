

class ExecutionContext:

    def __init__(self):

        self.observations = []

        self.variables = {}

    def add(
        self,
        tool: str,
        result,
    ):

        self.observations.append(
            {
                "tool": tool,
                "result": result,
            }
        )

    def all(
        self,
    ):

        return self.observations
    
    def set(
        self,
        name: str,
        value,
    ):

        self.variables[name] = value

    def get(
        self,
        name: str,
    ):

        return self.variables.get(
            name,
        )

    def memory(
        self,
    ):

        return self.variables

    