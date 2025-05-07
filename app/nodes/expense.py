from pocketflow import Node
from app.utils.gemini_client import GeminiClient


class CreateExpense(Node):
    @classmethod
    def get_function_declaration(cls):
        return {
            "name": "create_expense",
            "description": "Creates a new expense entry",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Date of the expense (YYYY-MM-DD)",
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount of the expense",
                    },
                    "expense_type": {
                        "type": "string",
                        "description": "Type of expense",
                    },
                    "vendor_id": {"type": "string", "description": "ID of the vendor"},
                },
                "required": ["date", "amount", "expense_type", "vendor_id"],
            },
        }

    def prep(self, shared):
        args = shared.get("function_args")
        if not args or not all(
            k in args for k in ["date", "amount", "expense_type", "vendor_id"]
        ):
            raise ValueError("Missing required expense arguments")
        return args

    def exec(self, args):
        # In a real implementation, this would call your expense creation API
        expense_id = f"EXPENSE_1"
        return expense_id

    def post(self, shared, prep_res, exec_res):
        result = "expense created with id: " + exec_res
        content = GeminiClient.content_from_function_response(
            role="user",
            function_name=shared["function_name"],
            response={"result": result},
        )
        shared["contents"].append(content)
        shared["results"].append(content)
