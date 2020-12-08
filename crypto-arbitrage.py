import ccxt
from twilio.rest import Client
import math

#kraken api- add your api keys below
kraken = ccxt.kraken({
    'apiKey': '*******',
    'secret': '*******',
})

#bitrex api- add your api keys below
bitrex = ccxt.bitrex({
    'apiKey': '*******',
    'secret': '*******',
})

#twilio sms api. Add your own api here
account_sid = '******'
auth_token = '*****'
client = Client(account_sid, auth_token)


def printsep():
    print("====================================================")


bittrex = ccxt.bittrex()
kraken = ccxt.kraken()

bittrex_markets = bittrex.load_markets()
kraken_markets = kraken.load_markets()

#find last price
kraken_price = kraken.fetch_ticker('BTC/USD')['close']

bitrex_price = bittrex.fetch_ticker('BTC/USD')['close']

#check on fees charged per transaction
kraken_fees = kraken.markets['BTC/USD']['maker']

bitrex_fees = bittrex.markets['BTC/USD']['maker']

#check for arbitraging
if kraken_price < bitrex_price:
	cross_exchange_arbitrage = (bitrex_price - kraken_price)/100
	buy = ("Buy on Kraken and sell on Bitrex. Your fees will be: " + str(kraken_fees))
	gain = bitrex_price - kraken_price
#	bittrex.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'})

#send an sms signal
	message = client.messages \
	.create(
                body="Buy Bitcoin on Kraken @ " + str(kraken_price) + " and sell on Bitrex @ " + str(bitrex_price) + " Arbitrage: " +  "{:.2f}".format(cross_exchange_arbitrage) + "%",
                from_= '+1*****',   #add your twilio number
                to= '+*******',     #add your cellnumber to receive sms
            )

else:
	cross_exchange_arbitrage = (kraken_price - bitrex_price)/100
	buy = ("Buy on Bittrex and sell on Kraken. Your fees will be: " + str(bitrex_fees))
	gain = kraken_price - bitrex_price
# 	kraken.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'})
		
	message = client.messages \
            .create(
            	body="Buy Bitcoin  on Bittrex @ " + str(kraken_price) + " and sell on Kraken @ " + str(bitrex_price) + " Arbitrage: " +  "{:.2f}".format(cross_exchange_arbitrage) + "%",
            	from_= '+1*****',   #add your twilio number
                to= '+*******',     #add your cellnumber to receive sms
            )

print("Cross Exchange Opportunity:",  buy, "your gain is: $", math.floor(gain))
print("Bittrex price is:", kraken_price,"---", "Kraken price is:", bitrex_price)
print("You arbitrage:", "{:.2f}".format(cross_exchange_arbitrage), "%")
printsep()  

# Here we start the code for buying and selling on a single exchange. Thresholds have to be set first as targets for trades.
sell_bitcoin_threshold = 19300 # change to the one you want
buy_bitcoin_threshold = 19045  #change to the one you want

if kraken_price <= buy_bitcoin_threshold:
	print("opportunity to buy Bitcoin on Kraken")
	#run a buy order on signal
#	kraken.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'}) 

elif kraken_price >= sell_bitcoin_threshold:
	print("Opportunity to sell Bitcoin on Bittrex")
#	kraken.create_market_sell_order('BTC/USD', 1, {'trading_agreement': 'agree'})

elif bitrex_price <= buy_bitcoin_threshold:
	print("Opportunity to buy Bitcoin on Kraken")
#	bitrex.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'})
	
elif bitrex_price >= sell_bitcoin_threshold:
	print("Opportunity to sell Bitcoin on Bittrex")
#	kraken.create_market_sell_order('BTC/USD', 1, {'trading_agreement': 'agree'})
	
else:
	print("No opportunities in single exchange is presented as yet")
