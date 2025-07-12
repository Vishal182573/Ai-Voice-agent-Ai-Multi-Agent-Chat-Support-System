from app.agents.support_agent import SupportAgent

class AgentRouter:
    def __init__(self, support_agent: SupportAgent):
        self.support_agent = support_agent

    def route(self, intent: str, query: str) -> str:
        """Routes the query to the correct handler based on the intent."""
        if intent == "FAQ":
            return self.support_agent.handle_faq(query)
        elif intent == "Complaint":
            return self.support_agent.handle_complaint(query)
        elif intent == "Account Inquiry":
            return self.support_agent.handle_account_inquiry(query)
        else: # Handles "General Inquiry" or any fallback
            return self.support_agent.handle_general_inquiry(query)