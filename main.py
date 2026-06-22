import ccxt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Android Finorix Bot")

# এক্সচেঞ্জ কানেকশন (Bybit/Binance)
# এখানে আপনার আসল API Key এবং Secret Key বসাবেন
exchange = ccxt.bybit({
    'apiKey': 'YOUR_API_KEY_HERE',
    'secret': 'YOUR_SECRET_KEY_HERE',
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'} # ফিউচার্স ট্রেডিংয়ের জন্য
})

class TradeSignal(BaseModel):
    symbol: str          
    side: str            
    amount: float        
    leverage: int = 10   
    take_profit: Optional[float] = None
    stop_loss: Optional[float] = None

@app.post("/webhook")
async def receive_signal(signal: TradeSignal):
    try:
        try:
            exchange.set_leverage(signal.leverage, signal.symbol)
        except Exception as le:
            print(f"Leverage Info: {le}")

        print(f"🚀 মোবাইল বট অর্ডার প্লেস করছে: {signal.side.upper()} {signal.symbol}")
        order = exchange.create_order(
            symbol=signal.symbol,
            type='market',
            side=signal.side.lower(),
            amount=signal.amount
        )
        
        params = {}
        if signal.stop_loss: params['stopLoss'] = signal.stop_loss
        if signal.take_profit: params['takeProfit'] = signal.take_profit
            
        if params:
            opposite_side = 'sell' if signal.side.lower() == 'buy' else 'buy'
            exchange.create_order(
                symbol=signal.symbol,
                type='market',
                side=opposite_side,
                amount=signal.amount,
                params=params
            )
            print("✅ TP/SL সেট সফল হয়েছে।")
            
        return {"status": "success", "order_id": order['id']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
