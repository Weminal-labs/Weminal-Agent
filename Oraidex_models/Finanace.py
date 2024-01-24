import numpy as np
from math import fabs

def getRSI(close, n=14):
    # compute a vector for change between daily closing prices
    change = np.zeros(len(close))
    for i in range(1, len(close)):
        change[i] = close[i] - close[i-1] ##Reversed the order of these.

    # compute a vector of gains and losses
    gain = np.zeros(len(close))
    loss = np.zeros(len(close))

    for i in range(1, len(close)):
        if change[i] >= 0:
            gain[i] = change[i]
            loss[i] = 0.00 ##Each array element needs a value.
        else:
            gain[i] = 0.00 ##Each array element needs a value.
            loss[i] = fabs(change[i])

    avg_gain = np.zeros(len(close) - n) ##Array length was wrong.
    avg_loss = np.zeros(len(close) - n) ##Array length was wrong.

    avg_gain[0] = np.average(gain[1:n+1]) ##First array element has a different calculation.
    avg_loss[0] = np.average(loss[1:n+1]) ##First array element has a different calculation.

    for i in range(1, len(close) - n): ##Loop counter was wrong.
        avg_gain[i] = (avg_gain[i-1]*(n-1) + gain[i+n])/n ##Indexes were wrong.
        avg_loss[i] = (avg_loss[i-1]*(n-1) + loss[i+n])/n ##Indexes were wrong.

    RS = np.zeros(len(close) - n) ##Array length was wrong.
    for i in range(0, len(close) - n): ##Loop counter was wrong.
        RS[i] = avg_gain[i]/avg_loss[i]

    RSI = np.zeros(len(close) - n) ##Array length was wrong.
    for i in range(0, len(close) - n): ##Loop counter was wrong.
        if avg_loss[i] == 0: ##This was missing. Could throw an error without it.
            RSI[i] = 100
        else:
            RSI[i] = 100 - (100/(1+RS[i]))

    return pad_like(RSI, close)


def sma(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def pad_like(input, thing_to_match):
    return np.pad(input, (len(thing_to_match) - len(input), 0), 'mean')