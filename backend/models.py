from pydantic import BaseModel


class Ticket(BaseModel):
    title: str
    description: str
    category: str
    priority: str
