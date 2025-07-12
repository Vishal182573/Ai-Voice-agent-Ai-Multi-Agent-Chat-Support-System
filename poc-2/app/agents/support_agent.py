from sqlalchemy.orm import Session
from app.db import models

class SupportAgent:
    def __init__(self, db_session: Session):
        self.db = db_session

    def handle_faq(self, query: str) -> str:
        # Mocked response for an FAQ
        return "Thank you for your question. For detailed FAQs, please visit our help center at help.example.com."

    def handle_account_inquiry(self, query: str) -> str:
        # Mocked response for an account inquiry
        return "For security reasons, please contact our support team directly at +1-800-555-0199 to discuss your account."

    def handle_complaint(self, query: str) -> str:
        # Creates a new ticket in the 'tickets' table. 
        new_ticket = models.Ticket(user_query=query, status="Open")
        self.db.add(new_ticket)
        self.db.commit()
        self.db.refresh(new_ticket)
        return f"We are sorry for the inconvenience. Your complaint has been registered with Ticket ID: {new_ticket.id}. Our team will investigate and get back to you shortly."

    def handle_general_inquiry(self, query: str) -> str:
        return "Thank you for contacting us. Can you please provide more details about your inquiry?"