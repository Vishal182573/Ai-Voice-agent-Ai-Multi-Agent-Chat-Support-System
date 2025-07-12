import google.generativeai as genai
from app.core.config import GEMINI_API_KEY

class AnalysisService:
    def __init__(self):
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            print(f"Error configuring Gemini: {e}")
            self.model = None

    def extract_intent_from_transcript(self, transcript: str, language: str = 'en') -> dict:
        if not self.model or not transcript:
            return {"intent": "Error", "summary": "Analysis model not available or empty transcript."}

        prompt = f"""
        Analyze the following customer support call transcript.
        The conversation language is {language}.
        Your task is to:
        1. Determine the primary intent of the user. Choose from: "Schedule Callback", "Resolve Issue", "General Inquiry", "Live Agent Request".
        2. Provide a concise one-sentence summary of the user's request.
        3. Format the response as a JSON object with keys "intent" and "summary".

        Transcript:
        ---
        {transcript}
        ---

        JSON Response:
        """
        try:
            response = self.model.generate_content(prompt)
            # Basic cleanup to extract JSON
            json_text = response.text.strip().replace("```json", "").replace("```", "").strip()
            import json
            return json.loads(json_text)
        except Exception as e:
            print(f"Error during Gemini analysis: {e}")
            return {"intent": "Analysis Failed", "summary": str(e)}