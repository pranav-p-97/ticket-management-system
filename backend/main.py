from fastapi import FastAPI
from models import Ticket

app = FastAPI(title="IT Ticket Management System")


@app.get("/")
def root():
    return {"message": "IT Ticket Management API is running"}


@app.post("/tickets")
def create_ticket(ticket: Ticket):
    return {
        "message": "Ticket created successfully",
        "ticket": ticket
    }
