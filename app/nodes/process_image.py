from pocketflow import Node
from typing import Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv
from app.models.expense import Expense
import os
import json

load_dotenv()

class ProcessImage(Node):
    def prep(self, shared):
        image_path = shared.get("file_path")
        return image_path

    def exec(self, image_path): 
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Gemini API key is required")

        client = genai.Client(api_key=api_key)

        prompt = f"""
        Task:
        Analyze the following invoice image and extract the expense details
        """

        try:
            # Read the image file
            with open(image_path, "rb") as f:
                image_bytes = f.read()

            # Create image part
            image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

            # Generate content with image and prompt
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[image_part, prompt],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": Expense,
                },
            )

            return json.loads(response.text)

        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")

    def post(self, shared, prep_res, exec_res):
        shared["expense"] = exec_res