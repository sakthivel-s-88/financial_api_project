import os
from dotenv import load_dotenv

load_dotenv()

#key Config
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#Vector DB StorAGE Config
CHROMA_DB_PATH = "./backend/storage/chroma_db"
CHROMA_COLLECTION_NAME = "financial_data"

#Data ingestion Config
TICKERS = ["AAPL", "GOOGL", "MSFT", "NVDA", "TSLA"]