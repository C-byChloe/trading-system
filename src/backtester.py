"""
Backtesting engine: simulates step-by-step trading logic,
tracks balance, PnL, and produces performance metrics.
"""

import numpy as np


class Backtester:
    def __init__(self, initial_balance=1000):
        self.initial_balance = initial_balance

    def run(self, prices, signals):
        balance = self.initial_balance
        position = 0
        equity_curve = []

        for i, (p, s) in enumerate(zip(prices, signals)):
            # Simple demo logic (user can modify)
            if s > 0 and position == 0:
                position = balance / p
                balance = 0
            elif s < 0 and position > 0:
                balance = position * p
                position = 0

            total_equity = balance + position * p
            equity_curve.append(total_equity)

        return equity_curve
