#!/usr/bin/env python3

from datetime import date, datetime
from decimal import Decimal
from functools import singledispatch  # using the singledispatch decorator
from json import  dumps


class Stock:
    '''
    :return: Stock object
    '''
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def toJSON(self):
        '''
        :return: Stock object dict
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

    # defining the equality method
    # to check the equality of the original dict and deserialized dicts
    def __eq__(self, other):
        return isinstance(other, Stock) and self.toJSON() == other.toJSON()

class Trade:
    '''
    :return: Trade object
    '''
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.commission = commission
        self.volume = volume

    def toJSONT(self):
        '''
        :return: Trade object dict
        '''
        return {
            'symbol' : self.symbol,
            'timestamp' : self.timestamp,
            'order' : self.order,
            'price' : self.price,
            'volume' : self.volume,
            'commission' : self.commission
        }

    # defining the equality method
    def __eq__(self, other):
        return isinstance(other, Trade) and self.toJSONT() == other.toJSONT()


# function to define how objects will be parsed
@singledispatch
def convert_to_json(arg):
    if isinstance(arg, set):
        return list(arg)
    elif isinstance(arg, date):
        return arg.strftime('%Y-%m-%d')
    else:
        return vars(arg)


@convert_to_json.register(datetime)
def _(arg):
    return arg.strftime('%Y-%m-%dT%H:%M:%S')


@convert_to_json.register(Stock)
def _(arg):
    obj = arg.toJSON()
    obj['object'] = arg.__class__.__name__
    return obj


@convert_to_json.register(Trade)
def _(arg):
    obj = arg.toJSONT()
    obj['object'] = arg.__class__.__name__
    return obj


@convert_to_json.register(Decimal)
def _(arg):
    return str(arg)



activity = {
    "quotes": [
        Stock('TSLA', date(2018, 11, 22), Decimal('338.19'), Decimal('338.64'),
              Decimal('337.60'), Decimal('338.19'), 365_607),
        Stock('AAPL', date(2018, 11, 22), Decimal('176.66'), Decimal('177.25'),
              Decimal('176.64'), Decimal('176.78'), 3_699_184),
        Stock('MSFT', date(2018, 11, 22), Decimal('103.25'), Decimal('103.48'),
              Decimal('103.07'), Decimal('103.11'), 4_493_689)
    ],
    "trades": [
        Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy',
              Decimal('338.25'), 100, Decimal('9.99')),
        Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell',
              Decimal('177.01'), 20, Decimal('9.99'))
    ]
}

# using the dumps method and printing out the string
# using the default arg to call the convert to json func
encode = dumps(activity, default=convert_to_json, indent=3)
#print(encode)