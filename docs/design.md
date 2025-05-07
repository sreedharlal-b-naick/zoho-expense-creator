# Zoho Expense Creator Design

## Overview

The Zoho Expense Creator is an AI-powered system that automates the process of creating expense entries in Zoho Books from various document formats. The system uses Gemini AI for document processing and follows an agent-based architecture where a central decision-making node orchestrates the flow of operations.

## System Architecture

```mermaid
flowchart TD
    A[Upload] --> B[Prepare]
    B --> C[Decide]
    C -->|get_vendor| D[GetVendor]
    C -->|create_vendor| E[CreateVendor]
    C -->|create_expense| F[CreateExpense]
    D -->|decide| C
    E -->|decide| C
```

## Components

### 1. Web Interface (Streamlit)
- **Purpose**: User-friendly interface for document upload and result visualization
- **Features**:
  - Document upload (PDF, images)
  - Processing status display
  - Result review and confirmation
  - Error handling and feedback

### 2. Node-based Processing
The system uses an agent-based architecture with the following nodes:

#### Upload Node
- `prep`: Validates file path from shared store
- `exec`: Uploads file using Gemini client
- `post`: Stores uploaded file in shared store

#### Prepare Node
- `prep`: Gets uploaded file from shared store
- `exec`: Prepares context and prompt for Gemini AI
- `post`: Stores prepared contents in shared store

#### Decide Node (Central Orchestrator)
- `prep`: Validates uploaded file and contents
- `exec`: Uses Gemini AI to analyze document and decide next action based on tools provided
- `post`: Routes to appropriate action based on decision

#### Action Nodes
- **GetVendor Node**:
  - `prep`: Validates vendor name
  - `exec`: Retrieves vendor information
  - `post`: Returns to decide node for next action
  - **Available Tools**:
  - `get_vendor(vendor_name)`: Retrieves vendor ID

- **CreateVendor Node**:
  - `prep`: Validates vendor details
  - `exec`: Creates new vendor
  - `post`: Returns to decide node for next action
  - **Available Tools**:
  - `create_vendor(vendor_name, gst_number)`: Creates new vendor

- **CreateExpense Node**:
  - `prep`: Validates expense details
  - `exec`: Creates expense entry
  - `post`: Stores result in shared store
  - **Available Tools**:
  - `create_expense(date, amount, expense_type, vendor_id)`: Creates expense entry

### 3. Shared Store
The system uses a shared store for communication between nodes:
```python
shared = {
    "file_path": "path/to/document",
    "uploaded_file": "file_content",
    "contents": [
        # List of Content objects for Gemini AI
    ],
    "function_name": "current_function",
    "function_args": {
        # Arguments for current function
    },
    "results": [
        # List of results from function calls
    ]
}
```


Each node implements appropriate error handling and validation in its `prep` and `exec` methods.

