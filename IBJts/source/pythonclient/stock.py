from IBJts.source.pythonclient.ibapi.client import EClient
from IBJts.source.pythonclient.ibapi.wrapper import EWrapper
from IBJts.source.pythonclient.ibapi.contract import Contract
from IBJts.source.pythonclient.ibapi.order import Order

class StockApp(EWrapper, EClient):

    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
        print("Error: ", reqId, errorCode, " ", errorString)

    def orderStatus(self, orderId: OrderId, status: str, filled: float,
                    remaining: float, avgFillPrice: float, permId: int,
                    parentId: int, lastFillPrice: float, clientId: int,
                    whyHeld: str, mktCapPrice: float):
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
        
        order = Order()
        order.action = 'BUY'
        order.totalQuantity = 500
        order.orderType = 'MKT'

        self.placeOrder(1, contract, order)


def main():
    app = StockApp()
    app.connect("127.0.0.1", 7497, 1)

    app.run()