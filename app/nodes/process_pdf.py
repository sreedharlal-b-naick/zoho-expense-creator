from pocketflow import Node
from typing import Dict, Any
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path
import os
import json
from app.models.expense import Expense

load_dotenv()


class ProcessPDF(Node):
    def prep(self, shared):
        pdf_path = shared.get("file_path")
        return pdf_path

    def exec(self, file_path: str) -> Dict[str, Any]:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key is required")

        client = genai.Client(api_key=api_key)
        prompt = f"""
        Task:
        Analyze the following PDF document and extract the expense details.
        """

        try:
            # Convert string path to Path object
            filepath = Path(file_path)

            file_part = types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type="application/pdf",
            )

            # Generate content with PDF and prompt
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[file_part, prompt],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Expense,
                },
            )

            return json.loads(response.text)

        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def post(self, shared, prep_res, exec_res):
        shared["expense"] = exec_res
