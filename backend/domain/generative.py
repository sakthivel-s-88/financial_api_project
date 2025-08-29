from langchain_google_genai import ChatGoogleGenerativeAI
from backend.config.settings import GOOGLE_API_KEY

def get_generative_model() -> ChatGoogleGenerativeAI:
    """Initializes and returns the Gemini model."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY, temperature=0.2)

def generate_summary(ticker: str, technical_indicators: dict, news_headlines: list) -> str:
    """Generates a high-level summary using technical and news data."""
    llm = get_generative_model()
    news_str = "\n".join(f"- {headline}" for headline in news_headlines)
    
    prompt = f"""
    Analyze the financial data for {ticker}. Provide a concise, one-paragraph summary for an investor,
    integrating the key technical points with the sentiment from the news.

    Technical Data:
    - Current Price: {technical_indicators.get('current_price')}
    - Key Trend: The price is currently trading {'above' if technical_indicators.get('price_vs_sma20_pct', 0) > 0 else 'below'} its 20-day SMA.
    - RSI Signal: {technical_indicators.get('rsi_signal')}

    Recent News Headlines:
    {news_str}

    Summary:
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Could not generate summary."