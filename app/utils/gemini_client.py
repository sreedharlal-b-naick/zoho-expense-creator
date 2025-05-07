from google import genai
from pathlib import Path
import os
from typing import Union, Optional, Any, Dict, List
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

    @staticmethod
    def content_from_function_call(
        role: str, function_call: genai.types.FunctionCall
    ) -> genai.types.Content:
        """
        Creates a Content object from a function call.

        Args:
            role: The role of the content (e.g., "model", "user")
            function_call: The function call to create content from

        Returns:
            A Content object containing the function call
        """
        return genai.types.Content(
            role=role, parts=[genai.types.Part(function_call=function_call)]
        )

    @staticmethod
    def content_from_function_response(
        role: str, function_name: str, response: Dict
    ) -> genai.types.Content:
        """
        Creates a Content object from a function response.

        Args:
            role: The role of the content (e.g., "model", "user")
            function_name: The name of the function that was called
            response: The response from the function call

        Returns:
            A Content object containing the function response
        """
        function_response_part = genai.types.Part.from_function_response(
            name=function_name, response=response
        )
        return genai.types.Content(role=role, parts=[function_response_part])

    def predict(
        self, contents: List[Any], tools: Optional[List[genai.types.Tool]] = None
    ) -> Dict:
        """
        Analyzes the contents and returns a function call if one is found.

        Args:
            contents: List of content objects to analyze
            tools: Optional list of tools to use. If not provided, uses default tools.

        Returns:
            Dict containing function name and arguments if a function call is found

        Raises:
            Exception: If no function call is found or if there's an error analyzing the content
        """
        try:
            if tools is None:
                tools = [
                    genai.types.Tool(
                        function_declarations=self.get_function_declarations()
                    )
                ]

            config = genai.types.GenerateContentConfig(
                tools=tools,
                automatic_function_calling=genai.types.AutomaticFunctionCallingConfig(
                    disable=True
                ),
            )

            response = self.client.models.generate_content(
                model="gemini-2.0-flash", contents=contents, config=config
            )

            for part in response.candidates[0].content.parts:
                if part.function_call:
                    return part.function_call

            raise Exception("No function call found in the response")

        except Exception as e:
            raise Exception(f"Error analyzing content: {str(e)}")

    def upload(self, filepath: Union[str, Path]) -> Any:
        """
        Upload a file (image or PDF) to Gemini.

        Args:
            filepath: Path to the file
            mime_type: Optional MIME type. If not provided, will be inferred from file extension
        """
        filepath = Path(filepath)

        if filepath.suffix.lower() in [".jpg", ".jpeg", ".png", ".pdf"]:
            return self.client.files.upload(file=filepath)
        else:
            raise ValueError(f"Unsupported file type: {filepath.suffix}")

    def complete(
        self, prompt: str, file: Any, response_schema: Optional[type] = None
    ) -> str:
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
            model="gemini-2.0-flash", contents=[file, prompt], config=config
        )

        return response.text
