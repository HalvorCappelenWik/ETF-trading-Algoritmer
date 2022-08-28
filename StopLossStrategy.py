# Trading strategy:
# We buy a stock or etf, then follow to create a trading stop loss order 5% below our price.
# If stop loss is hit, exit our position and wait 1 month before entering the market again.  

from curses import noecho
from datetime import datetime
from AlgorithmImports import *

class StopLossStrategy(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021,1,1)
        self.SetEndDate(2022,1,1)
        self.SetCash(100000)

        self.qqq = self.AddEquity("QQQ", Resolution.Hour).Symbol

        self.entryTicket = None
        self.stopMarketTicket = None
        self.entryTime = datetime.min
        self.stopMarketOrderFillTime = datetime.min
        self.highestPrice = 0


        # Method is called every time algo gets new data 
    def OnData(self, Data: Slice):
        
        # after last exit --> wait 30 days
        if (self.Time - self.stopMarketOrderFillTime).days < 30:
            return

        price = self.Securities[self.qqq].Price

        # send entry limit order 
        if not self.Portfolio.Invested and not self.Transactions.GetOpenOrders(self.qqq):
            quantity = self.CalculateOrderQuantity(self.qqq, 0.9)
            self.entryTicket = self.LimitOrder(self.qqq,quantity,price, "Entry Order")
            self.entryTime = self.Time

        
        # move limit price if not filled after 1 day 
        if (self.Time - self.entryTime).days > 1 and self.entryTicket.Status != OrderStatus.Filled:
            self.entryTime = self.Time
            updateFields = UpdateOrderFields()
            updateFields.LimitPrice = price
            self.entryTicket.Update(updateFields)

        # move up trailing stop price
        if self.stopMarketTicket is not None and self.Portfolio.Invested:
            if price > self.highestPrice:
                self.hightesPrice = price
                updateFields = UpdateOrderFields()
                updateFields.StopPrice = price * 0.95
                self.stopMarketTicket.Update(updateFields) 

        # Method is called on every order event
    def OnOrderEvent(self, orderEvent: OrderEvent):
        if orderEvent.Status != OrderStatus.Filled:
            return
        
        # if entry limit order is filled --> send stop loss order 
        if self.entryTicket is not None and self.entryTicket.OrderId == orderEvent.OrderId:
            self.stopMarketTicket = self.StopMarketOrder(self.qqq, -self.entryTicket.Quantity, 0.95*self.entryTicket.AverageFillPrice)
        
        # save fill time of stop loss order 
        if self.stopMarketTicket is not None and self.stopMarketTicket.OrderId == orderEvent.OrderId:
            self.stopMarketOrderFillTime = self.Time
            self.highestPrice = 0