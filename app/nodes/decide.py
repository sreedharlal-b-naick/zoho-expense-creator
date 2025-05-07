from pocketflow import Node
from google.genai import types
from typing import List
from app.utils.gemini_client import GeminiClient


class Decide(Node):
    def __init__(self, tools: List[types.Tool] = None):
        super().__init__()
        self.gemini_client = GeminiClient()
        self.tools = tools

    def prep(self, shared):
        uploaded_file = shared.get("uploaded_file")
        if not uploaded_file:
            raise ValueError("No uploaded file found in shared store")
        return shared

    def exec(self, shared):
        contents = shared.get("contents")
        try:
            function_call = self.gemini_client.predict(contents, self.tools)

            # Create content with function call
            content = GeminiClient.content_from_function_call("model", function_call)
            shared["contents"].append(content)
            shared["results"].append(content)

            return {"function": function_call.name, "args": function_call.args}

        except Exception as e:
            raise Exception(f"Error analyzing file: {str(e)}")

    def post(self, shared, prep_res, exec_res):
        shared["function_name"] = exec_res["function"]
        shared["function_args"] = exec_res["args"]
        return exec_res["function"]
