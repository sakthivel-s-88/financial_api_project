import yfinance as yf
from langchain_core.documents import Document
import feedparser
from urllib.parse import quote_plus

def fetch_financial_documents(tickers: list[str]) -> list[Document]:
    """
    Loads company info from yfinance and news from Google News RSS
    for a list of tickers.
    """
    print(f"Loading data for tickers: {tickers}...")
    documents = []
    for ticker_symbol in tickers:
        try:
            # 1. Get company info from yfinance
            ticker = yf.Ticker(ticker_symbol)
            info = ticker.info
            company_name = info.get('longName', ticker_symbol)
            
            info_doc_content = (
                f"Company Information for {company_name} ({ticker_symbol}):\n"
                f"Business Summary: {info.get('longBusinessSummary', 'N/A')}"
            )
            documents.append(Document(page_content=info_doc_content, metadata={"source": "company_info", "ticker": ticker_symbol}))

            # 2. Get news from Google News RSS
            print(f"Fetching news for {company_name} from Google News RSS...")
            query = f"{company_name} stock when:14d"
            encoded_query = quote_plus(query)
            rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
            
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:10]:
                # --- FIX: Safely get the publisher name ---
                try:
                    publisher = entry.source.title
                except AttributeError:
                    publisher = "N/A" # Fallback value if source or title is missing
                # --- END FIX ---

                news_doc_content = f"Title: {entry.title}\nPublisher: {publisher}"
                documents.append(Document(
                    page_content=news_doc_content,
                    metadata={"source": "news", "ticker": ticker_symbol, "link": entry.link}
                ))

        except Exception as e:
            print(f"Could not load data for {ticker_symbol}: {e}")
            
    print(f"Successfully loaded {len(documents)} documents.")
    return documents