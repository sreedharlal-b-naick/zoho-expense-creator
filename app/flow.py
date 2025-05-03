from pocketflow import Flow
from nodes.process_image import ProcessImage
from nodes.process_pdf import ProcessPDF


def process_expense(file_path: str, file_type: str) -> dict:
    """Process an expense file (image or PDF) and return the extracted data"""
    shared = {"file_path": file_path}

    # Create the appropriate node based on file type
    if file_type in ["jpg", "jpeg", "png"]:
        process_node = ProcessImage()
    elif file_type == "pdf":
        process_node = ProcessPDF()
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # Create and run the flow
    flow = Flow(start=process_node)
    flow.run(shared)

    return shared.get("expense")
