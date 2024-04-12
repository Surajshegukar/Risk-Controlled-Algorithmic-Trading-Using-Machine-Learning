import requests
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.stream import TradingStream
from alpaca.broker.models.accounts import Account
from alpaca import data
from aiohttp.web_routedef import post
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from exceptiongroup._catch import catch



api_key = "PKCQVBJHOJJ5WXGCYAY7"
secret = "oU1GTKtP6uW8pKHFBlzYM4BbzhkndzsN70ILdZ9N"
alp_base_url = 'https://paper-api.alpaca.markets/v2'
header = { 
            'APCA-API-KEY-ID' : api_key,
            'APCA-API-SECRET-KEY' : secret}


client = TradingClient(api_key,secret,paper=True)


# Get account information
def get_account():
    account = dict(client.get_account())
    for k,v in account.items():
        print(f"{k:30}--{v}")

# Put in an order
def order(symbol="SPY", qty=1, side=OrderSide.BUY):
    order_details = MarketOrderRequest(symbol=symbol, qty=qty, side=side, time_in_force=TimeInForce.DAY)
    order = client.submit_order(order_details)
    return order

# steam of trades
trades = TradingStream(api_key, secret, paper=True)
print("trades Status : ")
async def trade_status(data):
    print(data)
trades.subscribe_trade_updates(trade_status)

 
#  Get all open orders

def get_orders():
    orders = client.get_orders(GetOrdersRequest(status=QueryOrderStatus.OPEN, limit=100))
    order = [(order.symbol, order.qty, order.side, order.filled_qty, order.status) for order in orders]
    print("Orders")
    print(f"{'Symbol':9}{'Qty':>4}{'Side':>4}{'Filled':>6}{'Status':>10}")
    print("-" * 34)
    for order in order:
        print(f"{order[0]:9}{order[1]:>4}{order[2]:>4}{order[3]:>6}{order[4]:>10}")

# Get all closed orders
def get_closed_orders():
    orders = client.get_orders(GetOrdersRequest(status=QueryOrderStatus.CLOSED, limit=100))
    order = [(order.symbol, order.qty, order.side, order.filled_qty, order.status) for order in orders]
    print("Orders")
    print(f"{'Symbol':9}{'Qty':>4}{'Side':>4}{'Filled':>6}{'Status':>10}")
    print("-" * 34)
    for order in order:
        print(f"{order[0]:9}{order[1]:>4}{order[2]:>4}{order[3]:>6}{order[4]:>10}")
        
# order("META", 10, OrderSide.BUY)

def sell_all():
        orders = client.get_orders(GetOrdersRequest(status=QueryOrderStatus.OPEN, limit=100))
        order = [(order.symbol, order.qty, order.side, order.filled_qty, order.status) for order in orders]
        for order in order:
            order_details = MarketOrderRequest(symbol=order[0], qty=order[1], side=OrderSide.SELL, time_in_force=TimeInForce.DAY)
            order = client.submit_order(order_details)
            

def sell(symbol, qty = 1):
    order_details = MarketOrderRequest(symbol=symbol, qty=qty, side=OrderSide.SELL, time_in_force=TimeInForce.DAY)
    order = client.submit_order(order_details)

# sell("META", 10)