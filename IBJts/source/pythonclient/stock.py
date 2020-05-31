from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order

from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime
import time
import json
import math

class StockApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.checkStocks, 'interval', seconds=5)
        scheduler.start()

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, errorCode, " ", errorString)

    def checkStocks(self):
        now = datetime.datetime.now()
        suburl = "immediate"

        if now > datetime.datetime(now.year, now.month, now.day, 15, 34, 50):
            suburl = "scheduled"

        headers = {
            "content-type": "application/json",
        }
        url = "http://localhost:5012/trade/" + suburl + "?trader=ib"
        params = {}

        try:
            response = requests.get(url, params=params, headers=headers)
            stock = response.json().get("stock")

            print(str(stock))

            if stock != "":

                self.buyStock(stock)
                orderData = {
                    "trade": response.json().get("trade"),
                    "stock": response.json().get("stock"),
                    "status": "success",
                    "company": response.json().get("company"),
                    "amount": 500
                }
                orderUrl = "http://localhost:5012/order?trader=ib"
                resp1 = requests.post(orderUrl, params=params, data=json.dumps(orderData), headers=headers)

                orderCountData = {
                    "trade": response.json().get("trade"),
                }
                orderCountUrl = "http://localhost:5012/order/count?trader=ib"
                resp2 = requests.post(orderCountUrl, params=params, data=json.dumps(orderCountData), headers=headers)

        except requests.ConnectionError:
            print("cannot request")

    def orderStatus(self, orderId, status, filled,
                    remaining, avgFillPrice, permId,
                    parentId, lastFillPrice, clientId,
                    whyHeld, mktCapPrice):
        super().orderStatus(orderId, status, filled, remaining,
                            avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        print("OrderStatus. Id:", orderId, "Status:", status, "Filled:", filled,
              "Remaining:", remaining, "AvgFillPrice:", avgFillPrice,
              "PermId:", permId, "ParentId:", parentId, "LastFillPrice:",
              lastFillPrice, "ClientId:", clientId, "WhyHeld:",
              whyHeld, "MktCapPrice:", mktCapPrice)

    def buyStock(self, stock):

        contract = Contract()
        contract.secType = 'STK'
        contract.currency = 'JPY'
        contract.exchange = 'TSEJ'
        contract.symbol=str(stock)
        
        order = Order()
        order.action = 'BUY'
        order.totalQuantity = 500
        order.orderType = 'MKT'

        self.placeOrder(math.ceil(time.time()), contract, order)


#def main():
#    print ("running!")
app = StockApp()
app.connect("127.0.0.1", 7496, 1)

app.run()