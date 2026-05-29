"""Data shapes for the food order API.

We use Pydantic models. A Pydantic model is a class that describes what fields
the data must have and their types. FastAPI uses it to check incoming requests
and to shape outgoing responses automatically.
"""

from pydantic import BaseModel, Field


class OrderRequest(BaseModel):
    """What the customer sends us when placing an order."""

    customer: str = Field(min_length=1, description="Name of the customer")
    items: list[str] = Field(min_length=1, description="List of item names ordered")


class OrderConfirmation(BaseModel):
    """What we send back after receiving an order."""

    order_id: str
    status: str = "received"
    customer: str
    items: list[str]
    size: str = "normal"  # "normal" or "large" — set by the Order Agent's decide step
