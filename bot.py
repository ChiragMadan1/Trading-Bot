import websocket, json, pprint, talib, numpy 

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.004

closings = []

in_position = False 

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closings

    print('recieved message')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    candle_closed = candle['x']
    open = candle['o']
    high = candle['h']
    low = candle['l']
    close = candle['c']

    if candle_closed:
        print("Candle closed at: {}".format(close))
        closings.append(float(close))

    print(closings)

    if len(closings) > RSI_PERIOD:
        np_closings = numpy.array(closings)
        rsi = talib.RSI(np_closings, RSI_PERIOD)
        print(rsi)

        last_rsi = rsi[-1]

        print("The current RSI is {}".format(last_rsi))

        if last_rsi > RSI_OVERBOUGHT:
            if in_position:
                print("SELL!")
            else:
                print("OVERBOUGHT BUT YOU DON'T OWN IT.")
        
        if last_rsi < RSI_OVERSOLD:
            if in_position:
                print("OVERSOLD BUT YOU OWN IT.")
            else:
                print("BUY!")

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()


