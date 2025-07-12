class NotifyAgent:
    def send_update(self, message: str):
        """Mocks sending an email or WhatsApp notification."""
        print("---")
        print(f"NOTIFICATION SENT: {message}")
        print("---")