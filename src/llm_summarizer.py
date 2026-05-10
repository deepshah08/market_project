import os
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None

def summarize_news(headline: str) -> str:
    """Summarizes news using Gemini API, or returns a default message if no key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or not genai:
        return f"AI Summary (Mock): Market impact for '{headline}' is neutral."
    
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Briefly summarize the potential Indian stock market impact of this headline in 1-2 sentences: {headline}"
        )
        return response.text
    except Exception as e:
        return f"AI Summary Error: {str(e)}"
