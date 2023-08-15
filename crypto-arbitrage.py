import ccxt
from twilio.rest import Client
import math
import ccxt  # Cryptocurrency Exchange Library
import time

# Replace with your actual API keys
api_key_exchange1 = 'YOUR_API_KEY1'
api_secret_exchange1 = 'YOUR_API_SECRET1'
api_key_exchange2 = 'YOUR_API_KEY2'
api_secret_exchange2 = 'YOUR_API_SECRET2'

exchange1 = ccxt.binance({'apiKey': api_key_exchange1, 'secret': api_secret_exchange1})
exchange2 = ccxt.kraken({'apiKey': api_key_exchange2, 'secret': api_secret_exchange2})

def get_balances(exchange):
    balances = exchange.fetch_balance()
    return balances['total']

def get_prices(exchange1, exchange2, symbol):
    ticker1 = exchange1.fetch_ticker(symbol)
    ticker2 = exchange2.fetch_ticker(symbol)
    return ticker1['bid'], ticker2['ask']

def execute_arbitrage(symbol):
    while True:
        try:
            balance_exchange1 = get_balances(exchange1)
            balance_exchange2 = get_balances(exchange2)

            bid_price, ask_price = get_prices(exchange1, exchange2, symbol)

            if bid_price > ask_price:
                amount_to_buy = min(balance_exchange2[symbol.split("/")[0]], balance_exchange1[symbol.split("/")[1]])
                if amount_to_buy > 0:
                    # Execute buy on exchange2 and sell on exchange1
                    exchange2.create_market_buy_order(symbol, amount_to_buy)
                    exchange1.create_market_sell_order(symbol, amount_to_buy)

                    print(f"Arbitrage opportunity found!")
                    print(f"Buy on Exchange2 at {ask_price} and sell on Exchange1 at {bid_price}")
                else:
                    print("Insufficient balance for arbitrage.")
            else:
                print("No arbitrage opportunity at the moment.")

            time.sleep(60)  # Wait for a minute before checking again

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    symbol = "BTC/USDT"  # Replace with the trading pair you're interested in
    execute_arbitrage(symbol)
