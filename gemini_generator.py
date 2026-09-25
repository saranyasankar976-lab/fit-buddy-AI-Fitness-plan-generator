import os
import google.generativeai as genai

# API Key Render la irunthu edukkum
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def generate_workout_gemini(prompt: str):
    try:
        # 2.5 model thaan ipo work aaguthu
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini 2.5 error: {e}")
        # 2.5 fail aana 2.0 try pannurom
        try:
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e2:
            print(f"Fallback error: {e2}")
            return f"""
            **Your Personalized Fitness Plan:**
            
            {prompt}
            
            **Workout:** 30 min Cardio + 20 min Strength + 10 min Stretching daily
            **Diet:** High protein, low sugar, balanced diet
            (AI temporarily busy, demo plan shown)
            """
