# Use this scropt to learn how to use history requests, indicators and plotting. 

# Theory 
# History Requests:
# We use history request to find early data about securities to be compared with our current data
# 
# Indicators:
# 100+ pre-built indicators 
# SMA, EMA, RSI, BollingerBands, Momentum, ATR, Stochastic, VWAP 

# Strategy: 
# Will trade VOO ETF
# first try to identyfi if VOO is in an uptrend or downtrend 
# To determine this we use simple movingaverage (SMA). Above SMA = uptrend, below SMA = downtrend
# In addition we compare the current price to its 52-week high and low
# If VOO uptrend + near high = buy (As much as possible) (below sma = sell)
# If VOO downtrend + near low = sell   
# All other cases = dont wont an active position. 

from AlgorithmImports import *
from datetime import *
from collections import deque


class SMAStrategyOnVOOTrade(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021,1,1)
        self.SetEndDate(2022,1,1)
        self.SetCash(100000)
        self.voo = self.AddEquity("VOO", Resolution.Daily).Symbol


        """
        self.sma = self.SMA(self.voo, 30, Resolution.Daily)
        closing_prices = self.History(self.voo, 30, Resolution.Daily)["close"]
        for time, price in closing_prices.loc[self.voo].items():
            self.voo.Update(time,price)
            """
        
        self.sma = CustomSimpleMovingAverage("CustomSMA", 30)
        self.RegisterIndicator(self.voo, self.sma, Resolution.Daily)



    def OnData(self, data:Slice):
        if not self.sma.IsReady:
            return 

        hist = self.History(self.voo, timedelta(365), Resolution.Daily)
        low = min(hist["low"])
        high = max(hist["high"])

        price = self.Securities[self.voo].Price

        if price * 1.05 >= high and self.voo.Current.Value < price:
            if not self.Portfolio[self.voo].IsLong:
                self.SetHoldings(self.voo, 1)

        elif price * 0.95 <= low and self.voo.Current.Value > price:
            if not self.Portfolio[self.voo].IsShort:
                self.SetHoldings(self.voo, -1)

        else:
            self.Liquidate()


        self.Plot("Benchmark", "52w-High", high)
        self.Plot("Benchmark", "52w-low", low)
        self.Plot("Benchmark", "VOO", self.voo.Value)


class CustomSimpleMovingAverage(PythonIndicator):
    
    def __init__(self, name, period):
        self.Name = name
        self.Time = datetime.min
        self.Value = 0
        self.queue = deque(maxlen=period)

    def Update(self, input):
        self.queue.appendleft(input.Close)
        self.Time = input.EndTime
        count = len(self.queue)
        self.Value = sum(self.queue) / count
        # returns true if ready
        return (count == self.queue.maxlen)



