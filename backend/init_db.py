from database import Base, engine
from db_models import TicketDB

Base.metadata.create_all(bind=engine)

print("Database tables created successfully")
