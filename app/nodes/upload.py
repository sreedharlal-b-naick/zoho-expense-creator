from pocketflow import Node
from app.utils.gemini_client import GeminiClient


class Upload(Node):
    def prep(self, shared):
        file_path = shared.get("file_path")
        if not file_path:
            raise ValueError("No file path provided in shared store")
        return file_path

    def exec(self, file_path):
        client = GeminiClient()
        try:
            uploaded_file = client.upload(file_path)
            return uploaded_file
        except Exception as e:
            raise Exception(f"Error uploading file: {str(e)}")

    def post(self, shared, prep_res, exec_res):
        shared["uploaded_file"] = exec_res
        return "default"
