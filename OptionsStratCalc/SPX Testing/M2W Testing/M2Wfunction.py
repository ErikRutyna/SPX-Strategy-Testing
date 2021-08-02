import csv
import datetime
import datetime as dt
import math
import os.path
import time


#    0         1          2        3     4     5       6      7
# strike,option_type,   bid,     ask,  delta,gamma,  theta,  vega
# 750,        C,       1346.2, 1363.4,   1,     ,   -0.0004,
def makeOptionSnapshotMapFromShortType(rootFilter=None, dateFilter=None, timeFilter=None, expirationFilter=None):
    # H:\Tickers\SPXW\2017-01-19\0931\2017-01-23
    rootDirectory = 'H:/Tickers/'
    optionSnapshotMap = {}
    fileName = rootDirectory + rootFilter + '/' + dateFilter + '/' + timeFilter.replace(':', '') + '/' + \
               expirationFilter + '/' + 'ShortUnderlyingOptionsIntervals_60sec_calcs_oi_level2_' + dateFilter + '.csv'

    if os.path.isfile(fileName):
        with open(fileName) as f:
            for line in f.readlines()[1:]:
                split = line.strip('\n').split(",")
                strike = split[0]

                if optionSnapshotMap.get(strike) is None:
                    tempList = [split]
                    optionSnapshotMap.update({strike: tempList})
                else:
                    tempList = optionSnapshotMap.get(strike)
                    tempList.append(split)
                    optionSnapshotMap.update({strike: tempList})
    else:
        print('Cant find file: ' + fileName)

    return optionSnapshotMap


#         0            1         2           3      4    5               6              7      8      9     10    11
# quote_datetime, expiration, strike, option_type, bid, ask, active_underlying_price, delta, gamma, theta, vega, root
# 16:15,2021-07-07,1200,C,3151.8,3163.9, 4358.1299, 0.9999,,, 0.0001,SPX
# 09:31,2021-07-07,1200,P,,0.05,4352.8,-0.0001,,,0.0003,SPXW
def makeOptionSnapshotMapFromLightType(filename, timeFilter=None, rootFilter=None, expirationFilter=None):
    optionSnapshotMap = {}

    with open(filename) as f:
        for line in f.readlines()[1:]:
            split = line.split(",")
            root = split[11].replace("\n", "")
            time = split[0]
            expiration = split[1]

            if (rootFilter is None or rootFilter == root) and (timeFilter is None or time >= timeFilter) and (
                    expiration is None or expiration == expirationFilter):
                strike = split[2]
                if optionSnapshotMap.get(time) is None:
                    tempList = [split]
                    tempStrikeMap = {strike: tempList}
                    tempExpMap = {expiration: tempStrikeMap}
                    optionSnapshotMap.update({time: tempExpMap})
                else:
                    tempExpMap = optionSnapshotMap.get(time)

                    if tempExpMap.get(expiration) is None:
                        tempList = [split]
                        tempStrikeMap = {strike: tempList}
                        tempExpMap.update({expiration: tempStrikeMap})
                        optionSnapshotMap.update({time: tempExpMap})
                    else:
                        tempStrikeMap = optionSnapshotMap.get(time).get(expiration)

                        if tempStrikeMap.get(strike) is None:
                            tempList = [split]
                            tempStrikeMap.update({strike: tempList})
                            tempExpMap.update({expiration: tempStrikeMap})
                            optionSnapshotMap.update({time: tempExpMap})
                        else:
                            tempList = tempStrikeMap.get(strike)
                            tempList.append(split)
                            tempStrikeMap.update({strike: tempList})
                            tempExpMap.update({expiration: tempStrikeMap})
                            optionSnapshotMap.update({time: tempExpMap})

    # print('Length of map is: ' + str(len(optionSnapshotMap)))
    return optionSnapshotMap


#    0         1          2        3     4     5       6      7
# strike,option_type,   bid,     ask,  delta,gamma,  theta,  vega
# 750,        C,       1346.2, 1363.4,   1,     ,   -0.0004,
def getAll0DteExpirationDates(ticker, dateFilter=None):
    expirationDates = []
    tickerDir = 'H:/Tickers/' + ticker + '/'
    for dir in os.listdir(tickerDir):
        zeroDteExpirationDir = tickerDir + dir + '/0931/' + dir
        if (dateFilter is None or dir > dateFilter) and os.path.isdir(zeroDteExpirationDir):
            expirationDates.append(dir)

    return expirationDates


#  0      1
# 09:31,4420.69
def getPricesForDate(rootFilter, dateFilter):
    # H:\Tickers\SPXW\2017-01-19\2017-01-19_prices.csv
    rootDirectory = 'H:/Tickers/'
    pricesMap = {}
    fileName = rootDirectory + rootFilter + '/' + dateFilter + '/' + dateFilter + '_prices.csv'

    if os.path.isfile(fileName):
        with open(fileName) as f:
            for line in f.readlines()[1:]:
                split = line.split(",")
                time = split[0]
                price = split[1].strip('\n')

                pricesMap.update({time: price})

    return pricesMap


#    0         1          2        3     4     5       6      7
# strike,option_type,   bid,     ask,  delta,gamma,  theta,  vega
# 750,        C,       1346.2, 1363.4,   1,     ,   -0.0004,
def getOptionRowForTimeStrikeType(optionSnapshotMap, time, strike, type):
    tempList = optionSnapshotMap.get(time).get(str(strike))

    if tempList is not None:
        for optionRow in tempList:
            if optionRow[1] == type:  # P or C
                return optionRow


#    0         1          2        3     4     5       6      7
# strike,option_type,   bid,     ask,  delta,gamma,  theta,  vega
# 750,        C,       1346.2, 1363.4,   1,     ,   -0.0004,
def getTotalCostForSpread(optionLegsList):
    cost = 0.0

    for optionLeg in optionLegsList:
        short = optionLeg[1] < 0
        long = optionLeg[1] > 0
        bid = parseS2F(optionLeg[0][2]) if len(optionLeg[0][2]) > 0 else None
        ask = parseS2F(optionLeg[0][3]) if len(optionLeg[0][3]) > 0 else None
        numberOfContracts = abs(optionLeg[1])

        if short and bid is not None:
            if ask is not None:
                cost -= ((bid + ask) / 2) * numberOfContracts
            else:
                cost -= bid * numberOfContracts
        elif long and ask is not None:
            if bid is not None:
                cost += ((bid + ask) / 2) * numberOfContracts
            else:
                cost += ask * numberOfContracts
        else:
            # print("Malformed leg: " + str(optionLeg))
            return None

    return cost


#    0         1          2        3     4     5       6      7
# strike,option_type,   bid,     ask,  delta,gamma,  theta,  vega
# 750,        C,       1346.2, 1363.4,   1,     ,   -0.0004,
def calculateOptionMetrics(optionLegsList, closePrice):
    profit = 0

    for optionLeg in optionLegsList:
        strike = parseS2F(optionLeg[0][0])
        put = optionLeg[0][1] == 'P'
        call = optionLeg[0][1] == 'C'
        short = optionLeg[1] < 0
        long = optionLeg[1] > 0
        numberOfContracts = abs(optionLeg[1])

        if put and short:
            if closePrice < strike:
                profit += (closePrice - strike) * numberOfContracts
        elif put and long:
            if closePrice < strike:
                profit += (strike - closePrice) * numberOfContracts
        elif call and short:
            if closePrice > strike:
                profit += (strike - closePrice) * numberOfContracts
        elif call and long:
            if closePrice > strike:
                profit += (closePrice - strike) * numberOfContracts

    return profit


def ClosePredic(T59, T58, T57):
    T59D1, T59D2 = DerivsCalc(T59, T58, T57)

    ApproxClose = T59 + T59D1 + T59D2

    T00D1, T00D2 = DerivsCalc(ApproxClose, T59, T58)

    SPXClosePredic = T59 + 1/2 * (T59D1 + T59D2 + T00D1 + T00D2)
    return SPXClosePredic


def DerivsCalc(T59, T58, T57):
    FirstDeriv = (3 * T59 - 4 * T58 + T57) / 2
    SecondDeriv = (T59 - 2 * T58 + T57)
    return FirstDeriv, SecondDeriv


def getStrikesForStrat(strat, startTime, width, size, pricesMap, optionSnapshotMap):
    tempStrikeList = []
    spot = float(pricesMap.get(startTime))

    # IFDM2W, IFUM2W, IFCM2W, IFPM2W, DoubleIFM2W, ICM2W
    if strat == 'IFDM2W':
        shortCall = [math.floor(spot / 5) * 5, 'C', -size]
        shortPut = [math.floor(spot / 5) * 5, 'P', -size]
        longCall = [shortCall[0] + width, 'C', size]
        longPut = [shortPut[0] - width, 'P', size]

        tempStrikeList = [shortCall, shortPut, longCall, longPut]
    elif strat == 'IFUM2W':
        shortCall = [math.ceil(spot / 5) * 5, 'C', -size]
        shortPut = [math.ceil(spot / 5) * 5, 'P', -size]
        longCall = [shortCall[0] + width, 'C', size]
        longPut = [shortPut[0] - width, 'P', size]

        tempStrikeList = [shortCall, shortPut, longCall, longPut]
    elif strat == 'IFPM2W':
        T59 = datetime.datetime.strptime(startTime, '%H:%M')
        T58 = (T59 + datetime.timedelta(minutes=-1)).strftime("%H:%M")
        T57 = (T59 + datetime.timedelta(minutes=-2)).strftime("%H:%M")

        predictedClose = ClosePredic(spot, float(pricesMap.get(str(T58))), float(pricesMap.get(str(T57))))

        shortStrikeCandidateCeil = math.ceil(spot / 5) * 5
        shortStrikeCandidateFloor = math.floor(spot / 5) * 5

        if abs(shortStrikeCandidateCeil - predictedClose) < abs(shortStrikeCandidateFloor - predictedClose):
            shortCall = [shortStrikeCandidateCeil, 'C', -size]
            shortPut = [shortStrikeCandidateCeil, 'P', -size]
        else:
            shortCall = [shortStrikeCandidateFloor, 'C', -size]
            shortPut = [shortStrikeCandidateFloor, 'P', -size]

        longCall = [shortCall[0] + width, 'C', size]
        longPut = [shortPut[0] - width, 'P', size]

        tempStrikeList = [shortCall, shortPut, longCall, longPut]
    elif strat == 'IFCM2W':
        shortStrikeCandidateCeil = math.ceil(spot / 5) * 5
        shortStrikeCandidateFloor = math.floor(spot / 5) * 5

        if abs(shortStrikeCandidateCeil - spot) < abs(shortStrikeCandidateFloor - spot):
            shortCall = [shortStrikeCandidateCeil, 'C', -size]
            shortPut = [shortStrikeCandidateCeil, 'P', -size]
        else:
            shortCall = [shortStrikeCandidateFloor, 'C', -size]
            shortPut = [shortStrikeCandidateFloor, 'P', -size]

        longCall = [shortCall[0] + width, 'C', size]
        longPut = [shortPut[0] - width, 'P', size]

        tempStrikeList = [shortCall, shortPut, longCall, longPut]
    elif strat == 'DoubleIFM2W':
        shortUpCall = [math.ceil(spot / 5) * 5, 'C', -size]
        shortUpPut = [math.ceil(spot / 5) * 5, 'P', -size]
        shortDownCall = [math.floor(spot / 5) * 5, 'C', -size]
        shortDownPut = [math.floor(spot / 5) * 5, 'P', -size]
        longCall = [shortUpCall[0] + width, 'C', 2 * size]
        longPut = [shortDownPut[0] - width, 'P', 2 * size]

        tempStrikeList = [shortUpCall, shortUpPut, shortDownCall, shortDownPut, longCall, longPut]
    elif strat == 'ICM2W':
        shortCall = [math.ceil(spot / 5) * 5, 'C', -size]
        shortPut = [math.floor(spot / 5) * 5, 'P', -size]
        longCall = [shortCall[0] + width, 'C', size]
        longPut = [shortPut[0] - width, 'P', size]

        tempStrikeList = [shortPut, shortCall, longCall, longPut]

    return tempStrikeList


def getTimesForStrat(strat, start, stop=None):
    tempTimeList = []
    startTime = datetime.datetime.strptime(start, '%H:%M')

    # IFDM2W, IFUM2W, IFCM2W, IFPM2W, DoubleIFM2W, ICM2W
    if strat in ['IFDM2W', 'IFUM2W', 'IFPM2W', 'IFCM2W', 'DoubleIFM2W', 'ICM2W']:
        tempTimeList = [start]

    if stop is not None:
        tempTimeList.append(stop)

    return tempTimeList


def getReturns(profit, risk, width):
    if risk > 0:
        return profit / risk
    else:
        return profit / width


def SPX_M2W_G(Date):
    # make the map from xx:xx time till close and SPX or SPXW ticker on yyyy-mm-dd expiration
    timeList = ['15:57', '15:58', '15:59', '16:00']

    optionSnapshotMap = {}

    for t in timeList:
        tempMap = makeOptionSnapshotMapFromShortType(rootFilter='SPXW', dateFilter=Date,
                                                     timeFilter=t, expirationFilter=Date)
        optionSnapshotMap.update({t: tempMap})

    pricesMap = getPricesForDate(rootFilter='SPXW', dateFilter=Date)

    if len(optionSnapshotMap) > 0:
        IFDList = WriteIF_G(optionSnapshotMap, pricesMap, Date, "D")
        IFUList = WriteIF_G(optionSnapshotMap, pricesMap, Date, "U")
        IFCList = WriteIF_G(optionSnapshotMap, pricesMap, Date, "C")
        IFDoubleList = WriteDoubleIF(optionSnapshotMap, pricesMap, Date)
        ICList = WriteIC_G(optionSnapshotMap, pricesMap, Date)
        IFPList = WriteIF_P(optionSnapshotMap, pricesMap, Date)

        return [IFDList, IFUList, IFCList, IFDoubleList, ICList, IFPList]


def SPX_M2W_G2(strat, width, date, size, startTime, stopTime=None):
    timeList = getTimesForStrat(strat, startTime, stopTime)

    optionSnapshotMap = {}

    for t in timeList:
        tempMap = makeOptionSnapshotMapFromShortType(rootFilter='SPXW', dateFilter=date,
                                                     timeFilter=t, expirationFilter=date)
        optionSnapshotMap.update({t: tempMap})

    pricesMap = getPricesForDate(rootFilter='SPXW', dateFilter=date)
    stratStrikeList = getStrikesForStrat(strat, startTime, width, size, pricesMap, optionSnapshotMap)

    if (optionSnapshotMap is not None and len(optionSnapshotMap) > 0) \
            and (stratStrikeList is not None and len(stratStrikeList) > 0) \
            and (pricesMap is not None and len(pricesMap) > 0) \
            and (timeList is not None and len(timeList) > 0):

        totalCredit, totalDebit, optionSpreadPnL, profit = runStratFromStartTimeToStopTime(optionSnapshotMap, stratStrikeList,
                                                                             pricesMap, startTime, stopTime)

        if strat == 'DoubleIFM2W':
            width = 15

        if totalCredit is not None and totalCredit < 0: #and a credit based trade if credit is positive, on a debit trade no need to check
            risk = totalCredit + width

            tradeInformation = [date, strat, profit, -totalCredit, risk, totalDebit, pricesMap.get('15:58'),
                                pricesMap.get(startTime), pricesMap.get('16:00'), width]

            rtrn = getReturns(profit, risk, width)

            tradeInformation.append(rtrn)

            if rtrn >= 0:
                tradeInformation.append(rtrn)
                tradeInformation.append(None)
            else:
                tradeInformation.append(None)
                tradeInformation.append(rtrn)

            for strike in stratStrikeList:
                tradeInformation.append(strike[0])
                tradeInformation.append(strike[1])
                tradeInformation.append(strike[2])

            return tradeInformation


#    0         1          2        3     4     5       6      7
# strike,option_type,   bid,     ask,  delta,gamma,  theta,  vega
# 750,        C,       1346.2, 1363.4,   1,     ,   -0.0004,
def runStratFromStartTimeToStopTime(optionSnapshotMap, stratStrikeList, pricesMap, startTime, stopTime):
    optionLegsList = []
    totalDebit = None
    optionSpreadPnL = None

    for strike in stratStrikeList:
        if strike is None or len(strike) < 3:
            print()

        optionLegsList.append(
            [getOptionRowForTimeStrikeType(optionSnapshotMap, startTime, strike[0], strike[1]), strike[2]])

    for optionRow in optionLegsList:
        if optionRow[0] is None:
            return None, None, None, None

    totalCredit = getTotalCostForSpread(optionLegsList)

    if totalCredit is not None:
        if stopTime is None:
            spxClose = float(pricesMap.get('16:00'))

            optionSpreadPnL = calculateOptionMetrics(optionLegsList, spxClose)
            profit = optionSpreadPnL - totalCredit
        else:
            optionLegsList = []

            for strike in stratStrikeList:
                optionLegsList.append(
                    [getOptionRowForTimeStrikeType(optionSnapshotMap, stopTime, strike[0], strike[1]), strike[2]])

            totalDebit = getTotalCostForSpread(optionLegsList)

            profit = totalDebit - totalCredit

        return totalCredit, totalDebit, optionSpreadPnL, profit,
    else:
        return None, None, None, None


def WriteDoubleIF(optionSnapshotMap, pricesMap, ExpDate):
    PreviousSpot = float(pricesMap.get('15:58'))
    Spot = float(pricesMap.get('15:59'))
    SPXClose = float(pricesMap.get('16:00'))

    Label = 'DoubleIF'

    shortStrikeUp = math.ceil(Spot / 5) * 5
    shortStrikeDown = math.floor(Spot / 5) * 5
    longCall = shortStrikeUp + 5
    longPut = shortStrikeDown - 5

    ShortPutCreditRowUp = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', shortStrikeUp, 'P'), -1]
    ShortCallCreditRowUp = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', shortStrikeUp, 'C'), -1]
    ShortPutCreditRowDown = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', shortStrikeDown, 'P'), -1]
    ShortCallCreditRowDown = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', shortStrikeDown, 'C'), -1]
    LongPutDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', longPut, 'P'), 2]
    LongCallDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', longCall, 'C'), 2]
    optionLegsList = [ShortPutCreditRowUp, ShortCallCreditRowUp, ShortPutCreditRowDown, ShortCallCreditRowDown,
                      LongPutDebitRow, LongCallDebitRow]

    for optionRow in optionLegsList:
        if optionRow[0] is None:
            # print('missing strikes on: ' + str(ExpDate))
            return

    TotalCredit = getTotalCostForSpread(optionLegsList)

    if TotalCredit is not None:
        Risk = TotalCredit + 15

        optionSpreadPnL = calculateOptionMetrics(optionLegsList, SPXClose)
        Profit = optionSpreadPnL - TotalCredit

        TradeInformation = [ExpDate, Label, Profit, -TotalCredit, Risk, float(pricesMap.get('15:57')), PreviousSpot,
                            Spot, SPXClose, \
                            shortStrikeUp, longCall, shortStrikeDown, longPut]

        return TradeInformation


def WriteIF_G(optionSnapshotMap, pricesMap, ExpDate, Direction):
    PreviousSpot = float(pricesMap.get('15:58'))
    Spot = float(pricesMap.get('15:59'))
    SPXClose = float(pricesMap.get('16:00'))

    Label = "ASDF"

    if Direction == "D":
        ShortStrike = math.floor(Spot / 5) * 5
        Label = "IFD"
    elif Direction == "U":
        ShortStrike = math.ceil(Spot / 5) * 5
        Label = "IFU"
    elif Direction == "C":
        ShortStrikeCandidateCeil = math.ceil(Spot / 5) * 5
        ShortStrikeCandidateFloor = math.floor(Spot / 5) * 5

        if abs(ShortStrikeCandidateCeil - Spot) < abs(ShortStrikeCandidateFloor - Spot):
            ShortStrike = ShortStrikeCandidateCeil
            Label = "IFC"
        else:
            ShortStrike = ShortStrikeCandidateFloor
            Label = "IFC"

    LongCall = ShortStrike + 5
    LongPut = ShortStrike - 5

    ShortPutCreditRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', ShortStrike, 'P'), -1]
    ShortCallCreditRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', ShortStrike, 'C'), -1]
    LongPutDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', LongPut, 'P'), 1]
    LongCallDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', LongCall, 'C'), 1]
    optionLegsList = [ShortPutCreditRow, ShortCallCreditRow, LongPutDebitRow, LongCallDebitRow]

    if ShortPutCreditRow[0] is not None and ShortCallCreditRow[0] is not None \
            and LongPutDebitRow[0] is not None and LongCallDebitRow[0] is not None:
        TotalCredit = getTotalCostForSpread(optionLegsList)
    else:
        # print("missing strikes on: " + str(ExpDate))
        return

    if TotalCredit is not None:
        Risk = TotalCredit + 5

        optionSpreadPnL = calculateOptionMetrics(optionLegsList, SPXClose)
        Profit = optionSpreadPnL - TotalCredit

        # Parameter checks - difference to strike & "momentum"

        # Parameter 1: abs(Spot - Strike) < $1.50
        if abs(Spot - ShortStrike) < 1.50:
            P1 = 1
        else:
            P1 = 0

        Diff2StrikeP = round(ShortStrike - Spot, 2)
        Diff2StrikeC = round(ShortStrike - Spot, 2)

        # Parameter 2: (Spot - Spot @ 15:58)
        P2 = PreviousSpot - Spot

        TradeInformation = [ExpDate, Label, Profit, -TotalCredit, Risk, float(pricesMap.get('15:57')), PreviousSpot,
                            Spot, SPXClose, \
                            ShortStrike, LongCall, ShortStrike, LongPut, P1, Diff2StrikeC, Diff2StrikeP, P2]

        return TradeInformation


def WriteIC_G(optionSnapshotMap, pricesMap, ExpDate):
    PreviousSpot = float(pricesMap.get('15:58'))
    Spot = float(pricesMap.get('15:59'))
    SPXClose = float(pricesMap.get('16:00'))
    Label = 'IC'

    # Grab our 4 strikes for the IC
    ShortPut = math.floor(Spot / 5) * 5
    ShortCall = math.ceil(Spot / 5) * 5
    LongPut = ShortPut - 5
    LongCall = ShortCall + 5

    ShortPutCreditRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', ShortPut, 'P'), -1]
    ShortCallCreditRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', ShortCall, 'C'), -1]
    LongPutDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', LongPut, 'P'), 1]
    LongCallDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', LongCall, 'C'), 1]
    optionLegsList = [ShortPutCreditRow, ShortCallCreditRow, LongPutDebitRow, LongCallDebitRow]

    if ShortPutCreditRow[0] is not None and ShortCallCreditRow[0] is not None \
            and LongPutDebitRow[0] is not None and LongCallDebitRow[0] is not None:
        TotalCredit = getTotalCostForSpread(optionLegsList)
    else:
        # print("missing strikes on: " + str(ExpDate))
        return

    if TotalCredit is not None:
        Risk = TotalCredit + 5

        optionSpreadPnL = calculateOptionMetrics(optionLegsList, SPXClose)
        Profit = optionSpreadPnL - TotalCredit

        # Parameter checks - difference to strike & "momentum"

        # Parameter 1: abs(Spot - Strike) < $1.50
        if abs(Spot - ShortPut) < 2.51:
            P1 = "P"
        else:
            P1 = "C"

        Diff2StrikeP = round(ShortPut - Spot, 2)
        Diff2StrikeC = round(ShortCall - Spot, 2)

        # Parameter 2: (Spot - Spot @ 15:58)
        P2 = PreviousSpot - Spot

        TradeInformation = [ExpDate, Label, Profit, -TotalCredit, Risk, float(pricesMap.get('15:57')), PreviousSpot,
                            Spot, SPXClose, \
                            ShortCall, LongCall, ShortPut, LongPut, P1, Diff2StrikeC, Diff2StrikeP, P2]

        return TradeInformation


def WriteIF_P(optionSnapshotMap, pricesMap, ExpDate):
    PreviousSpot = float(pricesMap.get('15:58'))
    Spot = float(pricesMap.get('15:59'))
    SPXClose = float(pricesMap.get('16:00'))
    T57 = float(pricesMap.get('15:57'))
    Label = "IFP"

    PredicedClose = ClosePredic(Spot, PreviousSpot, T57)

    ShortStrikeCandidateCeil = math.ceil(Spot / 5) * 5
    ShortStrikeCandidateFloor = math.floor(Spot / 5) * 5

    if abs(ShortStrikeCandidateCeil - PredicedClose) < abs(ShortStrikeCandidateFloor - PredicedClose):
        ShortStrike = ShortStrikeCandidateCeil
    else:
        ShortStrike = ShortStrikeCandidateFloor

    LongCall = ShortStrike + 5
    LongPut = ShortStrike - 5

    ShortPutCreditRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', ShortStrike, 'P'), -1]
    ShortCallCreditRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', ShortStrike, 'C'), -1]
    LongPutDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', LongPut, 'P'), 1]
    LongCallDebitRow = [getOptionRowForTimeStrikeType(optionSnapshotMap, '15:59', LongCall, 'C'), 1]
    optionLegsList = [ShortPutCreditRow, ShortCallCreditRow, LongPutDebitRow, LongCallDebitRow]

    if ShortPutCreditRow[0] is not None and ShortCallCreditRow[0] is not None \
            and LongPutDebitRow[0] is not None and LongCallDebitRow[0] is not None:
        TotalCredit = getTotalCostForSpread(optionLegsList)
    else:
        # print("missing strikes on: " + str(ExpDate))
        return

    if TotalCredit is not None:
        Risk = TotalCredit + 5

        optionSpreadPnL = calculateOptionMetrics(optionLegsList, SPXClose)
        Profit = optionSpreadPnL - TotalCredit

        # Parameter checks - difference to strike & "momentum"

        # Parameter 1: abs(Spot - Strike) < $1.50
        if abs(Spot - ShortStrike) < 1.50:
            P1 = 1
        else:
            P1 = 0

        Diff2StrikeP = round(ShortStrike - Spot, 2)
        Diff2StrikeC = round(ShortStrike - Spot, 2)

        # Parameter 2: (Spot - Spot @ 15:58)
        P2 = PreviousSpot - Spot

        TradeInformation = [ExpDate, Label, Profit, -TotalCredit, Risk, T57, PreviousSpot, Spot, SPXClose, \
                            ShortStrike, LongCall, ShortStrike, LongPut, P1, Diff2StrikeC, Diff2StrikeP, P2]

        return TradeInformation


def SPX_M2W(Filename):
    print('Running SPX_M2W for: ' + Filename)

    """Generates a file consisting of returns for doing M2W trades on SPX using historical data.

    Extended Summary
    ----------------
    Checks the returns on a given 0DTE day for what the possible returns would be for a M2W trade
    (a IC or IF trade placed at 15:59 PM EST). Uses a set of parameters to apporiximate direction SPX
    is going so it can decided whether or not to place the IC or IF trade. Information regarding
    each trade is then printed to a CSV file.

    Parameters
    ----------

    Filename: string
        Filename consisting of that day's data from CBOE in a standardized CSV format for each row:
        [time, expiration date, strike, C/P flag, bid, ask, spot price, delta, gamma, theta, vega, root]

    Returns
    -------
    FullList: list
        Function returns a 3x16 sized list to be written to a csv file. Each row are the results for a different
        type of trade, 2x IF's at different strikes, and the last is an IC. Each row has the same format of:
        [date, trade type (IF/IC), P/L, Credit, Risk, Spot@15:58, Spot@15:59, Spot@16:00, short call strike, ...
        long call strike, short put strike, long put strike, check 1, difference to short put, ...
        difference to short call, "momentum"]
    """
    Date = Filename[len(Filename) - 5:len(Filename) - 15:-1]
    # Date is in YYYY-MM-DD format
    ExpDate = Date[::-1]
    Date = Date[::-1]

    # Check to see if M/W/F, skip to next day if we're not M/W/F, also skipping market holidays
    Date = dt.datetime(int(Date[0:4]), int(Date[5:7]), int(Date[8::]))
    if Date.strftime("%a") == "Tue" or Date.strftime("%a") == "Thu":
        return

        # make the map from xx:xx time till close and SPX or SPXW ticker on yyyy-mm-dd expiration
    optionSnapshotMap = makeOptionSnapshotMapFromLightType(Filename, '15:57', 'SPXW', ExpDate)

    if len(optionSnapshotMap) > 0:
        # Find spot price at 15:59 EST
        Spot = \
            optionSnapshotMap.get('15:59').get(ExpDate).get(
                list(optionSnapshotMap.get('15:59').get(ExpDate).keys())[0])[0][
                6]

        IFDList = WriteIF(optionSnapshotMap, float(Spot), ExpDate, "D")
        IFUList = WriteIF(optionSnapshotMap, float(Spot), ExpDate, "U")
        IFCList = WriteIF(optionSnapshotMap, float(Spot), ExpDate, "C")
        ICList = WriteIC(optionSnapshotMap, float(Spot), ExpDate)

        # print(IFUList)
        FullList = [IFDList, IFUList, IFCList, ICList]
        return FullList


def parseS2F(string):
    if len(string) == 0:
        return 0.0
    else:
        return float(string)


def WriteIF(OptionsChain, Spot, ExpDate, Direction):
    """Runs a M2W IF on SPX at the closest strike above the spot price of SPX at 15:59 EST,
    and writes results to a CSV file.

    Extended Summary
    ----------------
    Records various parameters on a given 0DTE day for what the possible returns and parameters for those
    returns would be for a M2W IF trade placed at 15:59 PM EST. Information regarding each trade is then
    printed to a CSV file.

    Parameters
    ----------

    OptionsChain: Dictionary
        The options chain for that day in list in dictionary form, with 3 keys: time, expiration date, and strike,
        The format for the list that is returned is:
        [time, expiration date, strike, C/P flag, bid, ask, spot price, delta, gamma, theta, vega, root]

    Spot: float
        The spot price of SPX at 15:59 EST on that specific day

    ExpDate: string
        Date of expiration in "YYYY-MM-DD" format

    Direction: char
        Whether or not we go up/down with the IF short strikes relative to the spot at 15:59 EST

    Returns
    -------
    TradeInformation: list
        List of the following information:
        [date, trade type (IF/IC), P/L, Credit, Risk, Spot@15:58, Spot@15:59, Spot@16:00, short call strike, ...
         long call strike, short put strike, long put strike, check 1, difference to short put, ...
         difference to short call, "momentum"]
    """
    # Strikes for the M2W IF using the closest strike above where SPX is trading
    Label = "ASDF"
    if Direction == "D":
        ShortStrike = math.floor(Spot / 5) * 5
        Label = "IFD"
    elif Direction == "U":
        ShortStrike = math.ceil(Spot / 5) * 5
        Label = "IFU"
    elif Direction == "C":
        ShortStrikeCandidateCeil = math.ceil(Spot / 5) * 5
        ShortStrikeCandidateFloor = math.floor(Spot / 5) * 5

        if abs(ShortStrikeCandidateCeil - Spot) < abs(ShortStrikeCandidateFloor - Spot):
            ShortStrike = ShortStrikeCandidateCeil
            Label = "IFC"
        else:
            ShortStrike = ShortStrikeCandidateFloor
            Label = "IFC"

    LongCall = ShortStrike + 5
    LongPut = ShortStrike - 5

    PreviousSpot = float(
        OptionsChain.get('15:58').get(ExpDate).get(list(OptionsChain.get('15:59').get(ExpDate).keys())[0])[0][6])
    SPXClose = float(
        OptionsChain.get('16:00').get(ExpDate).get(list(OptionsChain.get('15:59').get(ExpDate).keys())[0])[0][6])

    ShortPutCredit = 0
    ShortCallCredit = 0
    LongPutDebit = 0
    LongCallDebit = 0

    if OptionsChain.get("15:59").get(ExpDate).get(str(ShortStrike)) is not None \
            and OptionsChain.get("15:59").get(ExpDate).get(str(LongPut)) is not None \
            and OptionsChain.get("15:59").get(ExpDate).get(str(LongCall)) is not None:
        for row in OptionsChain.get("15:59").get(ExpDate).get(str(ShortStrike)):
            if row[3] == "P" and len(row[4]) > 0:
                ShortPutCredit = (parseS2F(row[4]) + parseS2F(row[5])) / 2
            else:
                ShortCallCredit = (parseS2F(row[4]) + parseS2F(row[5])) / 2

        for row in OptionsChain.get("15:59").get(ExpDate).get(str(LongPut)):
            if row[3] == 'P' and len(row[5]) > 0:
                LongPutDebit = (parseS2F(row[4]) + parseS2F(row[5])) / 2

        for row in OptionsChain.get("15:59").get(ExpDate).get(str(LongCall)):
            if row[3] == 'C' and len(row[5]) > 0:
                LongCallDebit = (parseS2F(row[4]) + parseS2F(row[5])) / 2
    else:
        # print("missing strikes on: " + str(ExpDate))
        return

    # Find the total amount of credit for the IF as well as the risk
    if ShortPutCredit == 0 or ShortCallCredit == 0 or LongPutDebit == 0 or LongCallDebit == 0:
        return

    TotalCredit = round(ShortPutCredit + ShortCallCredit - LongPutDebit - LongCallDebit, 2)

    if TotalCredit >= 5:
        Risk = -(TotalCredit - 5)
    else:
        Risk = 5 - TotalCredit

    # Break evens
    # UpperBE = ShortStrike + TotalCredit
    # LowerBE = ShortStrike - TotalCredit

    # Check if we're in the breakeven zone for profit
    if abs(ShortStrike - SPXClose) > 5:
        Profit = -Risk
    else:
        Profit = TotalCredit - abs(ShortStrike - SPXClose)

    Profit = round(Profit, 2)

    # Parameter checks - difference to strike & "momentum"

    # Parameter 1: abs(Spot - Strike) < $1.50
    if abs(Spot - ShortStrike) < 1.50:
        P1 = 1
    else:
        P1 = 0

    Diff2StrikeP = round(ShortStrike - Spot, 2)
    Diff2StrikeC = round(ShortStrike - Spot, 2)

    # Parameter 2: (Spot - Spot @ 15:58)
    P2 = PreviousSpot - Spot

    TradeInformation = [ExpDate, Label, Profit, TotalCredit, Risk, PreviousSpot, Spot, SPXClose, \
                        ShortStrike, LongCall, ShortStrike, LongPut, P1, Diff2StrikeC, Diff2StrikeP, P2]

    return TradeInformation


def WriteIC(OptionsChain, Spot, ExpDate):
    """Runs a M2W IC on SPX and writes results to a CSV file.

    Extended Summary
    ----------------
    Records various parameters on a given 0DTE day for what the possible returns and parameters for those
    returns would be for a M2W IC trade placed at 15:59 PM EST. Information regarding each trade is then
    printed to a CSV file.

    Parameters
    ----------

    OptionsChain: list
        The options chain for that day in list form, and each row consists of
        [time, expiration date, strike, C/P flag, bid, ask, spot price, delta, gamma, theta, vega, root]

    Spot: float
        The spot price of SPX at 15:59 EST on that specific day

    MaxIndex: int
        Maximum index for iteration to speed up the loops

    Returns
    -------

    Function does not return anything directly, instead it write results to a CSV file.
    """
    # Grab our 4 strikes for the IC
    ShortPut = math.floor(Spot / 5) * 5
    ShortCall = math.ceil(Spot / 5) * 5
    LongPut = ShortPut - 5
    LongCall = ShortCall + 5

    # Additional close information
    Label = "IC"
    PreviousSpot = float(
        OptionsChain.get('15:58').get(ExpDate).get(list(OptionsChain.get('15:59').get(ExpDate).keys())[0])[0][6])
    SPXClose = float(
        OptionsChain.get('16:00').get(ExpDate).get(list(OptionsChain.get('15:59').get(ExpDate).keys())[0])[0][6])

    ShortPutCredit = 0
    ShortCallCredit = 0
    LongPutDebit = 0
    LongCallDebit = 0

    if OptionsChain.get("15:59").get(ExpDate).get(str(ShortPut)) is not None \
            and OptionsChain.get("15:59").get(ExpDate).get(str(ShortCall)) is not None \
            and OptionsChain.get("15:59").get(ExpDate).get(str(LongPut)) is not None \
            and OptionsChain.get("15:59").get(ExpDate).get(str(LongCall)) is not None:
        for row in OptionsChain.get("15:59").get(ExpDate).get(str(ShortPut)):
            if row[3] == "P" and len(row[4]) > 0:
                ShortPutCredit = (parseS2F(row[4]) + parseS2F(row[5])) / 2

        for row in OptionsChain.get("15:59").get(ExpDate).get(str(ShortCall)):
            if row[3] == "C" and len(row[4]) > 0:
                ShortCallCredit = (parseS2F(row[4]) + parseS2F(row[5])) / 2

        for row in OptionsChain.get("15:59").get(ExpDate).get(str(LongPut)):
            if row[3] == 'P' and len(row[5]) > 0:
                LongPutDebit = (parseS2F(row[4]) + parseS2F(row[5])) / 2

        for row in OptionsChain.get("15:59").get(ExpDate).get(str(LongCall)):
            if row[3] == 'C' and len(row[5]) > 0:
                LongCallDebit = (parseS2F(row[4]) + parseS2F(row[5])) / 2
    else:
        # print("missing strikes on: " + str(ExpDate))
        return

    # Find the total amount of credit for the IF as well as the risk
    if ShortPutCredit == 0 or ShortCallCredit == 0 or LongPutDebit == 0 or LongCallDebit == 0:
        return

    TotalCredit = round(ShortPutCredit + ShortCallCredit - LongPutDebit - LongCallDebit, 2)

    if TotalCredit >= 5:
        Risk = -(TotalCredit - 5)
    else:
        Risk = 5 - TotalCredit

    # Break evens
    # UpperBE = ShortCall + TotalCredit
    # LowerBE = ShortPut - TotalCredit

    # Check if we're in the breakeven zone for profit
    # Full profit
    if (SPXClose <= ShortCall) and (SPXClose >= ShortPut):
        Profit = TotalCredit
    # Partial on call side
    elif (SPXClose > ShortCall and SPXClose < LongCall):
        Profit = TotalCredit - abs(SPXClose - ShortCall)
    # Partial on put side
    elif (SPXClose < ShortPut and SPXClose > LongPut):
        Profit = TotalCredit - abs(SPXClose - ShortPut)
    # Maximum loss
    elif (SPXClose > LongCall) or (SPXClose < LongPut):
        Profit = -Risk

    Profit = round(Profit, 2)

    # Parameter checks - difference to strike & "momentum"

    # Parameter 1: abs(Spot - Strike) < $2.51 -
    # for IC's this is kind of a useless parameter, but we're keeping it
    if abs(Spot - ShortPut) < 2.51:
        P1 = "P"
    else:
        P1 = "C"

    Diff2StrikeP = round(ShortPut - Spot, 2)
    Diff2StrikeC = round(ShortCall - Spot, 2)

    # Parameter 2: (Spot - Spot @ 15:58)
    P2 = PreviousSpot - Spot

    TradeInformation = [ExpDate, Label, Profit, TotalCredit, Risk, PreviousSpot, Spot, SPXClose, \
                        ShortCall, LongCall, ShortPut, LongPut, P1, Diff2StrikeC, Diff2StrikeP, P2]

    return TradeInformation


def main():
    # filenames = next(walk('H:\CboeLightCSV'), (None, None, []))[2]
    # filenamesFiltered = []

    # for file in filenames:
    #    date = file[len(file) - 5:len(file) - 15:-1]
    #   date = date[::-1]
    #
    #   if date >= "2016-09-01":
    #      filenamesFiltered.append('H:/CboeLightCSV/' + file)

    # filenamesFiltered = 'H:/CboeLightCSV/LightUnderlyingOptionsIntervals_60sec_calcs_oi_level2_2016-09-01.csv'

    # makeOptionSnapshotMapFromLightType(filenamesFiltered, '15:57', 'SPXW')

    start2 = time.time()
    zeroDTEs = getAll0DteExpirationDates('SPXW')

    # with concurrent.futures.ThreadPoolExecutor(24) as executor:
    #    resultsMain = list(executor.map(SPX_M2W_G, zeroDTEs))
    resultsMain = []
    strats = ['IFDM2W', 'IFUM2W', 'IFCM2W', 'IFPM2W', 'DoubleIFM2W', 'ICM2W']
    for strat in strats:
        print(strat)
        for zeroDTE in zeroDTEs:
            resultsMain.append(SPX_M2W_G2(strat=strat, width=5, date=zeroDTE, size=1, startTime='15:59', stopTime=None))

    # for zeroDTE in zeroDTEs:
    #    resultsMain.append(SPX_M2W_G(zeroDTE))

    totalMapTime = time.time() - start2
    print(totalMapTime)

    # SPX_M2W_G('2016-09-02')

    # with concurrent.futures.ProcessPoolExecutor(12) as executor:
    #   resultsMain = list(executor.map(SPX_M2W, filenamesFiltered))

    resultsFinal = []
    for result in resultsMain:
        if result is not None:
            resultsFinal.append(result)

    with open("outM2W.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        headers = ['Date', 'Trade Type', 'P/L', 'Credit', 'Risk', 'Spot@15:57', 'Spot@15:58', 'Spot@15:59',
                   'Spot@16:00', 'Width', 'Return', 'Positive Return', 'Negative Return']

        differenceInSize = int((len(max(resultsFinal, key=len)) - len(headers)) / 3)
        for i in range(1, differenceInSize + 1):
            headers.append('Strike ' + str(i))
            headers.append('Strike ' + str(i) + ' Option Type')
            headers.append('Strike ' + str(i) + ' Size')

        writer.writerows([headers])
        writer.writerows(resultsFinal)

    # print(results)


if __name__ == '__main__':
    main()
