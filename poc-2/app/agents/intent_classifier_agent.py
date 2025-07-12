import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

class IntentClassifierAgent:
    def __init__(self):
        # Configure the Gemini API client
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            self.model = None

    def classify_intent(self, query: str) -> str:
        if not self.model:
            return "Error: Gemini model not initialized"

        # These are the specific support agents we have
        # Defines the categories for classification. 
        valid_intents = ["FAQ", "Complaint", "Account Inquiry"]

        # The prompt guides the model to perform the classification task
        prompt = f"""
        Given the user query, classify it into one of the following categories: {', '.join(valid_intents)}.
        Respond with ONLY the category name. If the query does not fit any category, classify it as 'General Inquiry'.

        Query: "{query}"
        Category:
        """
        try:
            response = self.model.generate_content(prompt)
            # Clean up the response to get only the intent text
            intent = response.text.strip()
            # Ensure the model's response is one of the valid intents
            if intent in valid_intents or intent == "General Inquiry":
                return intent
            else:
                # Fallback if the model returns an unexpected value
                return "General Inquiry"
        except Exception as e:
            print(f"Error during Gemini API call: {e}")
            # Fallback to a default intent in case of an API error
            return "General Inquiry"