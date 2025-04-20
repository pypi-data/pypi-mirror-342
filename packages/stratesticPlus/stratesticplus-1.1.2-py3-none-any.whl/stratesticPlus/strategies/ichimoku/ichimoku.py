from collections import OrderedDict
from stratesticPlus.backtesting import VectorizedBacktester
from stratesticPlus.strategies._mixin import StrategyMixin
import pandas as pd
import numpy as np

class IchimokuCloud(StrategyMixin):
    """
    Ichimoku Cloud Strategy:
    This strategy uses Ichimoku Cloud components to generate trading signals.
    """

    def __init__(self, tenkan_period=9, kijun_period=26, senkou_b_period=52, data=None, **kwargs):
        self._tenkan_period = tenkan_period
        self._kijun_period = kijun_period
        self._senkou_b_period = senkou_b_period

        # Set default OHLC column names (changed to lowercase to match typical data formats)
        self._high_col = 'high'
        self._low_col = 'low'
        self._close_col = 'close'

        self.params = OrderedDict(
            tenkan_period=lambda x: int(x),
            kijun_period=lambda x: int(x),
            senkou_b_period=lambda x: int(x)
        )

        StrategyMixin.__init__(self, data, **kwargs)

    def update_data(self, data):
        data = super().update_data(data)

        high = data[self._high_col]
        low = data[self._low_col]
        close = data[self._close_col]

        # Calculate Ichimoku indicators
        data['tenkan_sen'] = (high.rolling(window=self._tenkan_period).max() + 
                              low.rolling(window=self._tenkan_period).min()) / 2
        data['kijun_sen'] = (high.rolling(window=self._kijun_period).max() + 
                             low.rolling(window=self._kijun_period).min()) / 2
        data['senkou_span_a'] = ((data['tenkan_sen'] + data['kijun_sen']) / 2).shift(self._kijun_period)
        data['senkou_span_b'] = ((high.rolling(window=self._senkou_b_period).max() + 
                                  low.rolling(window=self._senkou_b_period).min()) / 2).shift(self._kijun_period)

        return self.calculate_positions(data)

    def calculate_positions(self, data):
        close = data[self._close_col]
        span_a = data['senkou_span_a']
        span_b = data['senkou_span_b']

        # Generate long (1) / short (-1) / neutral (0) positions
        data['side'] = np.where(close > span_a, 1, np.nan)
        data['side'] = np.where(close < span_b, -1, data['side'])
        data['side'] = data['side'].ffill().fillna(0)
        return data

    def get_signal(self, row=None):
        if row is None:
            row = self.data.iloc[-1]
        return int(row['side'])

