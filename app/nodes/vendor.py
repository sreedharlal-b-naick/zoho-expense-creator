from pocketflow import Node
from google.genai import types
from app.utils.gemini_client import GeminiClient


class CreateVendor(Node):
    @classmethod
    def get_function_declaration(cls):
        return {
            "name": "create_vendor",
            "description": "Creates a new vendor with name and GST number",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendor_name": {
                        "type": "string",
                        "description": "Name of the vendor",
                    },
                    "gst_number": {
                        "type": "string",
                        "description": "GST number of the vendor",
                    },
                },
                "required": ["vendor_name", "gst_number"],
            },
        }

    def prep(self, shared):
        args = shared.get("function_args")
        if not args or "vendor_name" not in args or "gst_number" not in args:
            raise ValueError("Missing required vendor arguments")
        return args

    def exec(self, args):
        # In a real implementation, this would call your vendor creation API
        vendor_id = f"VENDOR_123"
        return vendor_id

    def post(self, shared, prep_res, exec_res):
        result = "vendor created with id: " + exec_res
        content = GeminiClient.content_from_function_response(
            role="user",
            function_name=shared["function_name"],
            response={"result": result},
        )
        shared["contents"].append(content)
        shared["results"].append(content)
        return "decide"


class GetVendor(Node):
    @classmethod
    def get_function_declaration(cls):
        return {
            "name": "get_vendor",
            "description": "Retrieves vendor ID by vendor name",
            "parameters": {
                "type": "object",
                "properties": {
                    "vendor_name": {
                        "type": "string",
                        "description": "Name of the vendor to look up",
                    }
                },
                "required": ["vendor_name"],
            },
        }

    def prep(self, shared):
        args = shared.get("function_args")
        if not args or "vendor_name" not in args:
            raise ValueError("Missing vendor name")
        return args

    def exec(self, args):
        # In a real implementation, this would call your vendor creation API
        # For now, we'll just return None. ie, vendor does not exist
        return "vendor does not exist"

    def post(self, shared, prep_res, exec_res):
        content = GeminiClient.content_from_function_response(
            role="user",
            function_name=shared["function_name"],
            response={"result": exec_res},
        )
        shared["contents"].append(content)
        shared["results"].append(content)
        return "decide"
