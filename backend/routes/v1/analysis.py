import yfinance as yf
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from backend.domain import technical_analysis, generative, news

router = APIRouter()

class AnalysisResponse(BaseModel):
    ticker: str
    technical_indicators: Dict[str, Any]
    high_level_summary: str

@router.get("/analysis/{ticker}", response_model=AnalysisResponse, tags=["Stock Analysis"])
async def get_full_analysis(ticker: str):
    #PerformING a full analysis on a given stock ticker
    try:
        price_data = yf.Ticker(ticker).history(period="6mo")
        if price_data.empty:
            raise HTTPException(status_code=404, detail="Could not fetch price data.")

        tech_indicators = technical_analysis.calculate_indicators(price_data)
        news_docs = news.fetch_financial_documents([ticker])
        news_headlines = [doc.page_content for doc in news_docs if doc.metadata.get('source') == 'news']
        
        summary = generative.generate_summary(ticker, tech_indicators, news_headlines)
        
        return AnalysisResponse(
            ticker=ticker,
            technical_indicators=tech_indicators,
            high_level_summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))