from pocketflow import Node
from google.genai import types


class Prepare(Node):
    def prep(self, shared):
        return shared

    def exec(self, shared):
        # Better to use uploaded file before the prompt in the
        uploaded_file = shared.get("uploaded_file")
        contents = [uploaded_file]

        prompt = f"""
        Task:
        Analyze the following invoice, provided context and create an expense entry. 
        
        Instructions:
        - Before creating the expense entry, you need to get the vendor ID.
        - If the vendor does not exist, you need to create the vendor first and then create the expense entry. 
        - Always start with getting the vendor ID.

        Available functions:
        - create_vendor(vendor_name, gst_number): Creates a new vendor
        - get_vendor(vendor_name): Gets vendor ID by name
        - create_expense(date, amount, expense_type, vendor_id): Creates expense entry

        Based on the invoice content, decide which function to call and with what parameters.
        """

        contents.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

        return contents

    def post(self, shared, prep_res, exec_res):
        shared["contents"] = exec_res
