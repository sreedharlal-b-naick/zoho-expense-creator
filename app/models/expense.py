from pydantic import BaseModel, Field


class Expense(BaseModel):
    date: str = Field(description="The date of the expense in YYYY-MM-DD format")
    amount: float = Field(
        description="The total expense amount as a number (no currency symbol)"
    )
    vendor: str = Field(description="The name of the vendor or company")
    expense_type: str = Field(
        description="A brief category like 'Travel', 'Meals', 'Office Supplies', etc."
    )
