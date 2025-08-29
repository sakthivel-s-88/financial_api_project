import pandas as pd
import pandas_ta as ta

def calculate_indicators(price_data: pd.DataFrame) -> dict:
    #Calculating the  technical indicators from a DataFrame of price data
    if price_data.empty:
        return {}

    price_data.ta.sma(length=20, append=True)
    price_data.ta.sma(length=50, append=True)
    price_data.ta.bbands(length=20, append=True)
    price_data.ta.rsi(length=14, append=True)
    
    latest = price_data.iloc[-1]
    
    sma_20_trend = "Bullish" if latest['Close'] > latest['SMA_20'] else "Bearish"
    rsi_signal = "Overbought" if latest['RSI_14'] > 70 else "Oversold" if latest['RSI_14'] < 30 else "Neutral"

    indicators = {
        "current_price": latest['Close'],
        "price_change": latest['Close'] - price_data.iloc[-2]['Close'],
        "sma_20": latest['SMA_20'],
        "sma_50": latest['SMA_50'],
        "rsi_14": latest['RSI_14'],
        "volatility_20d_bbw": latest['BBB_20_2.0'],
        "price_vs_sma20_pct": ((latest['Close'] - latest['SMA_20']) / latest['SMA_20']) * 100,
        "sma_20_trend": sma_20_trend,
        "rsi_signal": rsi_signal
    }
    
    return {key: round(value, 2) if isinstance(value, (int, float)) else value for key, value in indicators.items()}