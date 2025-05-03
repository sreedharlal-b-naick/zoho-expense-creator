# Zoho Expense Creator

An AI-powered agent that automatically creates expense entries in Zoho Books from expense documents (PDFs/images).

## Features

- Extract expense information from PDFs and images using Gemini AI
- Validate expense data against Zoho Books categories
- Create expense entries in Zoho Books automatically
- Handle errors and retries gracefully
- Support for multiple document formats
- Web UI for easy document upload and processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zoho-expense-creator.git
cd zoho-expense-creator
```

2. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Set up environment variables:
Create a `.env` file in the project root with:
```bash
GEMINI_API_KEY="your_gemini_api_key"
```

## Usage

### Web UI
Run the web interface:
```bash
poetry run web
```
This will start a Streamlit web app where you can:
- Upload expense documents
- View extraction results
- Review and confirm expense entries
- Track processing status

## License

MIT License
