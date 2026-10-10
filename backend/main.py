from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from models import Ticket
from database import get_db
from db_models import TicketDB

app = FastAPI(title="IT Ticket Management System")


@app.get("/")
def root():
    return {"message": "IT Ticket Management API is running"}


@app.post("/tickets")
def create_ticket(ticket: Ticket, db: Session = Depends(get_db)):
    new_ticket = TicketDB(
        title=ticket.title,
        description=ticket.description,
        category=ticket.category,
        priority=ticket.priority
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket": {
            "id": new_ticket.id,
            "title": new_ticket.title,
            "description": new_ticket.description,
            "category": new_ticket.category,
            "priority": new_ticket.priority
        }
    }


@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(TicketDB).all()
    return tickets


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@app.put("/tickets/{ticket_id}")
def update_ticket(
    ticket_id: int,
    ticket: Ticket,
    db: Session = Depends(get_db)
):
    existing_ticket = db.query(TicketDB).filter(
        TicketDB.id == ticket_id
    ).first()

    if existing_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    existing_ticket.title = ticket.title
    existing_ticket.description = ticket.description
    existing_ticket.category = ticket.category
    existing_ticket.priority = ticket.priority

    db.commit()
    db.refresh(existing_ticket)

    return {
        "message": "Ticket updated successfully",
        "ticket": {
            "id": existing_ticket.id,
            "title": existing_ticket.title,
            "description": existing_ticket.description,
            "category": existing_ticket.category,
            "priority": existing_ticket.priority
        }
    }


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketDB).filter(TicketDB.id == ticket_id).first()

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted successfully",
        "ticket_id": ticket_id
    }
