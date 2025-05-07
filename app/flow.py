from pocketflow import Flow
from google.genai import types
from app.nodes.upload import Upload
from app.nodes.prepare import Prepare
from app.nodes.decide import Decide
from app.nodes.vendor import CreateVendor, GetVendor
from app.nodes.expense import CreateExpense


def process_expense(file_path: str) -> dict:
    """Process an expense file (image or PDF) and return the extracted data"""

    shared = {"file_path": file_path, "results": []}
    function_declarations = [
        CreateVendor.get_function_declaration(),
        GetVendor.get_function_declaration(),
        CreateExpense.get_function_declaration(),
    ]
    tools = [types.Tool(function_declarations=function_declarations)]

    upload = Upload()
    prepare = Prepare()
    decide = Decide(tools=tools)
    get_vendor = GetVendor()
    create_vendor = CreateVendor()
    create_expense = CreateExpense()

    upload >> prepare >> decide

    # Connect the nodes
    # If DecideAction returns "get_vendor", go to GetVendor
    decide - "get_vendor" >> get_vendor

    # If DecideAction returns "create_vendor", go to CreateVendor
    decide - "create_vendor" >> create_vendor

    # If DecideAction returns "create_expense", go to CreateExpense
    decide - "create_expense" >> create_expense

    # After GetVendor completes and returns "decide", go back to DecideAction
    get_vendor - "decide" >> decide

    # After CreateVendor completes and returns "decide", go back to DecideAction
    create_vendor - "decide" >> decide

    # Create and run the flow
    flow = Flow(start=upload)
    flow.run(shared)

    return shared.get("results", None)
