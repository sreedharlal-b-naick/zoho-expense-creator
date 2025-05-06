from google import genai
from pathlib import Path
import os
from typing import Union, Optional, Any
from dotenv import load_dotenv

load_dotenv()

class GeminiClient:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not GeminiClient._initialized:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Gemini API key is required")
            self.client = genai.Client(api_key=api_key)
            GeminiClient._initialized = True

    def upload(self, filepath: Union[str, Path]) -> Any:
        """
        Upload a file (image or PDF) to Gemini.
        
        Args:
            filepath: Path to the file
            mime_type: Optional MIME type. If not provided, will be inferred from file extension
        """
        filepath = Path(filepath)

        if filepath.suffix.lower() in ['.jpg', '.jpeg', '.png', '.pdf']:
            return self.client.files.upload(file=filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath.suffix}")

    def complete(self, prompt: str, file: Any, response_schema: Optional[type] = None) -> str:
        """
        Generate content using the uploaded file and prompt.
        
        Args:
            prompt: The prompt to use with the file
            response_mime_type: Optional MIME type for the response
            response_schema: Optional schema for structured response
            
        Returns:
            The generated response text
        """

        config = {"response_mime_type": "application/json"}
        if response_schema:
            config["response_schema"] = response_schema

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[file, prompt],
            config=config
        )

        return response.text