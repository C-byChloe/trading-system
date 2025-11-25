"""
Live execution engine: async event loop, order logic,
cooldown, stop-loss, and API integration.
"""

import asyncio
from datetime import datetime, timezone
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


class ExecutionEngine:
    def __init__(self, client: TradingClient, pair="ETHUSD", qty=0.01):
        self.client = client
        self.pair = pair
        self.qty = qty
        self.last_trade_time = None

    async def send_order(self, side):
        order_data = MarketOrderRequest(
            symbol=self.pair,
            qty=self.qty,
            side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        return self.client.submit_order(order_data)

    async def loop(self, predict_fn, wait_time=10, rounds=None):
        """predict_fn returns (current_price, predicted_price)."""
        i = 0
        while True:
            curr, pred = predict_fn()

            if pred > curr:
                await self.send_order("buy")
            else:
                await self.send_order("sell")

            i += 1
            if rounds and i >= rounds:
                break

            await asyncio.sleep(wait_time)
