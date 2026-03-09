import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Force load from current directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Configure Gemini API
# The user should provide an API key in the environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("DEBUG: Gemini API configured.")
else:
    print(f"DEBUG: Gemini API key NOT found. Checked path: {env_path}")

def process_content(text):
    """
    Passes text to Gemini and returns (structured JSON content, error_message).
    """
    if not text:
        return None, "No text provided"
        
    if not GEMINI_API_KEY:
        error = "GEMINI_API_KEY not found in environment. Please check your .env file."
        return None, error

    # Trim extremely long text to avoid potential prompt issues
    # 50k characters is more than enough for a summary and quiz.
    if len(text) > 50000:
        print(f"DEBUG: Trimming text from {len(text)} to 50000 characters.")
        text = text[:50000] + "... [Text trimmed to stay within processing limits]"

    prompt = f"""
    You are an expert educational content creator. Analyze the provided text and transform it into a high-quality learning suite.
    
    Return a valid JSON object with the following structure:
    {{
        "summary": "A concise and engaging summary of the content.",
        "concepts": ["key concept 1", "key concept 2", ...],
        "quiz": [
            {{
                "question": "A multiple-choice question testing understanding.",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "The exact correct option string"
            }},
            ... (at least 3-5 questions)
        ],
        "keywords": ["subject classification keywords (e.g., Physics, History, etc.)"]
    }}
    
    Text to process:
    {text}
    """

    # List of models to try in order of preference
    models_to_try = [
        'gemini-1.5-flash',
        'gemini-2.5-flash-lite', # Newer version seen in user environment
        'gemini-pro',           # Classic fallback
        'gemini-pro-latest'
    ]
    
    last_error = ""
    for model_name in models_to_try:
        try:
            print(f"DEBUG: Trying model: {model_name}")
            model = genai.GenerativeModel(model_name,
                                         generation_config={"response_mime_type": "application/json"})
            
            response = model.generate_content(prompt)
            # Parse the JSON response
            try:
                data = json.loads(response.text)
                return data, None
            except json.JSONDecodeError as je:
                print(f"Error: JSON Parse Error from {model_name}: {je}")
                return None, f"AI returned invalid JSON: {je}"
        except Exception as e:
            last_error = str(e)
            print(f"DEBUG: Model {model_name} failed: {last_error}")
            # If the error is a 404 or specific model error, try the next one
            if "404" in last_error or "not found" in last_error.lower() or "503" in last_error:
                continue 
            else:
                # If it's an API key error or something fatal, stop early
                return None, last_error
    
    return None, f"All AI models failed. last error: {last_error}"
