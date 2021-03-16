#!/usr/bin/env python3

from datetime import date, datetime
from decimal import Decimal
from json import JSONEncoder, dump, dumps, load, loads



class Stock:
    '''
    creating the Stock class
    '''
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

        # Todo : add a toJson method here
    def toJSON(self):
        '''
        :return: stock object
        type: dict
        '''
        return {
            'symbol': self.symbol,
            'date': self.date,
            'open': self.open,
            'high' : self.high,
            'low' : self.low,
            'close' : self.close,
            'volume' : self.volume
        }

class Trade:
    '''
    Trade class to create the Trade instance
    '''
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.commission = commission
        self.volume = volume

    # Todo : add a toJson method here
    def toJSON(self):
        '''
        Method to return the trade object as a dict (can use vars here too)
        :return: type dict
        '''
        return {
            'symbol' : self.symbol,
            'timestamp' : self.timestamp,
            'order' : self.order,
            'price' : self.price,
            'volume' : self.volume,
            'commission' : self.commission
        }


class CustomEncoder(JSONEncoder):
    '''
    Creating a custom encoder class
    '''
    def default(self, arg):
        if isinstance(arg, Stock) or isinstance(arg, Trade):
            obj =  arg.toJSON()
            obj['object'] = arg.__class__.__name__
            return obj
        elif isinstance(arg, datetime):
            return arg.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(arg, date):
            return arg.strftime('%Y-%m-%d')
        elif isinstance(arg, Decimal):
            return str(arg)
        else:
            return super().default(arg)

# creating a python dictionary
activity = {
    "quotes": [
        Stock('TSLA', date(2018, 11, 22), Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607),
        Stock('AAPL', date(2018, 11, 22), Decimal('176.66'), Decimal('177.25'), Decimal('176.64'), Decimal('176.78'), 3_699_184),
        Stock('MSFT', date(2018, 11, 22), Decimal('103.25'), Decimal('103.48'), Decimal('103.07'), Decimal('103.11'), 4_493_689)
    ],
    "trades": [
        Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99')),
        Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell', Decimal('177.01'), 20, Decimal('9.99'))
    ]
}

# the dictionary is passed to the json.dumps with the CustomEncoder class defining how the dict is serialized

encode = dumps(activity, cls=CustomEncoder, indent=3)
print(encode)

