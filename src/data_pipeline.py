"""
Data ingestion & preprocessing pipeline.

This module wraps market data fetching, cleaning, scaling, 
and feature window creation.
"""

import pandas as pd
import numpy as np
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame


class DataPipeline:
    def __init__(self, pair="ETH/USD", hours=720):
        self.pair = pair
        self.hours = hours
        self.client = CryptoHistoricalDataClient()

    def fetch(self):
        """Fetch historical bars from Alpaca."""
        req = CryptoBarsRequest(
            symbol_or_symbols=self.pair,
            timeframe=TimeFrame.Hour,
        )
        df = self.client.get_crypto_bars(req).df
        df = df[df.index.get_level_values("symbol") == self.pair]
        return df

    def get_feature(self, df):
        """Select the feature to feed into the model."""
        return df[["close"]].values
