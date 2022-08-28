# region imports
from datetime import timedelta
from AlgorithmImports import *
# endregion

class SPYTradingBot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 2, 26)  # Set Start Date
        self.SetEndDate(2022, 8, 10) # Set end date
        self.SetCash(100000)  # Set Strategy Cash, for BackTesting purposes.

        spy = self.AddEquity("SPY", Resolution.Daily)
        # self.AddForex, self.Addfuture

        spy.SetDataNormalizationMode(DataNormalizationMode.Raw) # No adjustment to asset price. 

        self.spy = spy.Symbol # To avoid ambiguety and be more secure.

        self.SetBenchmark("SPY") # Setting a benchmark for the algorithm. Since trading SPY, SPY becomes benchmark. Will generate a chart for backtesting.

        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin) # Setting my Brokerage model. Could use cash accouint, but use margin. 

        # Custome varables. 
        self.entryPrice = 0   # Track our entry price.           
        self.period = timedelta(31) # Period set to 31 days. 
        self.nextEntryTime = self.Time # When we should reentry SPY position. 


                 
    def OnData(self, data: Slice):

        # Check if requested data does exist 
        # SPY actively traded so wont be a problem 
        if not self.spy in data:
            return

        # price = data.Bars[self.spy].Close  # Closeprice from prev day
        price = data[self.spy].Close
        # price = self.Securities[self.spy].Close

        # Trade Logic
        # Check if bot is invested
        if not self.Portfolio.Invested:
            # Check if time to invest 
            if self.nextEntryTime <= self.Time:
                # If time, we buy as much SPY as we can 
                self.SetHoldings(self.spy,1)
                # self.MarketOrder(self.spy, int(self.Portfolio.Cash / price) )

                # Log our transaction and price. Helpful for reviewing and debugging
                self.Log("JUST BOUGHT SPY @" + str(price))

                # Update the current price of SPY to the entry price to be used for exit condition. 
                self.entryPrice = price
        
        # Exit Process 
        # Check if entry price it 10% below or above current price. 
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            # self.Liquidate will liquidate all our SPY holding. We log our transaction and exit price.
            self.Liquidate(self.spy)
            self.Log("JUST SOLD SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period # Re entry in 31 days
