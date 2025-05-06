from pocketflow import Flow
from app.nodes.process import Process


def process_expense(file_path: str, file_type: str) -> dict:
    """Process an expense file (image or PDF) and return the extracted data"""
    
    shared = {"file_path": file_path}
    process_node = Process()

    # Create and run the flow
    flow = Flow(start=process_node)
    flow.run(shared)

    return shared.get("expense")
