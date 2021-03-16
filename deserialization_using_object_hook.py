#!/usr/bin/env python3

from datetime import date, datetime
from decimal import Decimal
from json import dumps, loads
from json_serialization_using_default import convert_to_json, Stock, Trade
from pprint import pprint


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

encode = dumps(activity, default=convert_to_json, indent=3)




def custom_decoder(obj):
    '''
    defining how objects will be decode
    :param obj: json string
    :return: dict
    '''
    dict_value = obj
    if 'object' in obj:
        if obj['object'] == 'Stock':
            dict_value = Stock(obj['symbol'], datetime.strptime(obj['date'], '%Y-%m-%d').date(),
                               Decimal(obj['open']), Decimal(obj['high']),
                              Decimal(obj['low']), Decimal(obj['close']), obj['volume'])
        elif obj['object'] == 'Trade':
            dict_value = Trade(obj['symbol'], datetime.strptime(obj['timestamp'], '%Y-%m-%dT%H:%M:%S'),
                               obj['order'], Decimal(obj['price']), obj['volume'], Decimal(obj['commission']))
    return dict_value


decode = loads(encode, object_hook=custom_decoder)
#print(decode)


new_dict = {}
for i in decode:
    counter = 0
    new_dict[i] = []
    for val in decode[i]:
        new_dict[i].append(vars(decode[i][counter]))
        counter += 1
pprint(new_dict)
