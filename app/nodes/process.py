from pocketflow import Node
from app.utils.gemini_client import GeminiClient
from app.models.expense import Expense
import json


class Process(Node):
    def prep(self, shared):
        file_path = shared.get("file_path")
        return file_path

    def exec(self, file_path): 
        client = GeminiClient()

        prompt = f"""
        Task:
        Analyze the following invoice and extract the expense details
        """

        try:
            file = client.upload(file_path)
            response = client.complete(prompt, file, Expense)
            return json.loads(response)

        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def post(self, shared, prep_res, exec_res):
        shared["expense"] = exec_res