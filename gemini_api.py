import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyB0NdB4kKvN-DxFSCtNwA1OBxGg0qsTbCk")  # Replace with your real key

def get_gemini_response(prompt):
    """Generate AI response using Gemini API."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text
