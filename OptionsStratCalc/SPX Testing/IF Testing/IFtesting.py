import concurrent
import csv
import datetime
import math
import os.path
import time


def SPX_SL_TP_Multi():
    resultsMain = None
    allExpiration = getExpirationDates(ticker='SPXW', isZeroDte=True)

    multi = True

    if multi:
        with concurrent.futures.ProcessPoolExecutor(10) as executor:
            resultsMain = list(executor.map(SPX_SL_TP, allExpiration))
    else:
        for expiration in allExpiration:
            print(expiration)
            SPX_SL_TP(expiration)

    return resultsMain


def SPX_SL_TP(expiration):
    print(expiration)
    ticker = 'SPXW'
    startTime = '10:00'
    stopTime = None#'12:00'
    width = 50
    start = '2016-09-01'
    end = '2021-07-07'
    dynamicTP = False

    timeList = ['09:31', '09:35', '09:40', '09:45']

    while '12:00' not in timeList:
        timeList.append(addMinutesToTimeAsStringReturnString(timeList[-1], 15))

    widthStart = 10
    widthMax = 50
    widthIncrement = 5

    widthList = []

    for i in range(widthStart, widthMax - 1, widthIncrement):
        widthList.append(i)

    stopLossStart = -2
    stopLossStop = -4
    stopLossIncrement = -1

    stopLossList = []

    for i in range(stopLossStart, stopLossStop - 1, stopLossIncrement):
        stopLossList.append(i)

    takeProfitList = []

    if dynamicTP:
        takeProfitStart = 5
        takeProfitStop = 100
        takeProfitIncrement = 5
    else:
        takeProfitStart = 13
        takeProfitStop = 13
        takeProfitIncrement = 1

    for i in range(takeProfitStart, takeProfitStop + 1, takeProfitIncrement):
        takeProfitList.append(i)

    SLTPWT = []

    for sl in stopLossList:
        for tp in takeProfitList:
            for w in widthList:
                for t in timeList:
                    SLTPWT.append([sl, tp, w, t])

    strats = ['IFDM2W', 'IFUM2W', 'IFCM2W']#, 'DoubleIFM2W', 'ICM2W']

    optionSnapshotMap = {}
    if stopTime is None:
        for t in generateFullDayOfTimes():
            tempMap = makeOptionSnapshotMapFromShortType(rootFilter=ticker, dateFilter=expiration,
                                                     timeFilter=t, expirationFilter=expiration)

            optionSnapshotMap.update({t: tempMap})
    else:
        tempMap = makeOptionSnapshotMapFromShortType(rootFilter=ticker, dateFilter=expiration,
                                                     timeFilter=startTime, expirationFilter=expiration)

        optionSnapshotMap.update({startTime: tempMap})

        tempMap = makeOptionSnapshotMapFromShortType(rootFilter=ticker, dateFilter=expiration,
                                                     timeFilter=stopTime, expirationFilter=expiration)

        optionSnapshotMap.update({stopTime: tempMap})

    results = []
    pricesMap = getPricesForDate(rootFilter=ticker, dateFilter=expiration)

    for strat in strats:
        for sltpwt in SLTPWT:
            stopLoss = sltpwt[0]
            takeProfit = sltpwt[1]
            width = sltpwt[2]
            startTime = sltpwt[3]

            stratStrikeList = getStrikesForStrat(strat=strat, startTime=startTime, width=width, size=1, pricesMap=pricesMap,
                                                 optionSnapshotMap=None)
            totalCredit, totalDebit, profit, stoppedTime = runStratWithStopLossTakeProfit(optionSnapshotMap=optionSnapshotMap, stratStrikeList=stratStrikeList,
                                           pricesMap=pricesMap, startTime=startTime, stopTime=stopTime, stopLoss=stopLoss, takeProfit=takeProfit, dynamicTP=dynamicTP)



            if totalCredit is not None and totalCredit < 0:  # and a credit based trade if credit is positive, on a debit trade no need to check
                risk = totalCredit + width

                tradeInformation = [expiration, strat.replace("M2W", str(stopLoss) + "/" + str(takeProfit) + "/" + str(width) + "/" + str(startTime)), profit, -totalCredit, risk, totalDebit, pricesMap.get(startTime),
                                    pricesMap.get(stoppedTime), stoppedTime]

                rtrn = getReturns(profit, risk, width)

                tradeInformation.append(rtrn)

                if rtrn >= 0:
                    tradeInformation.append(rtrn)
                    tradeInformation.append(None)
                else:
                    tradeInformation.append(None)
                    tradeInformation.append(rtrn)

                #for strike in stratStrikeList:
                #    tradeInformation.append(strike[0])
                #    tradeInformation.append(strike[1])
                #    tradeInformation.append(strike[2])

                results.append(tradeInformation)

    return results


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


def getReturns(profit, risk, width):
    if risk > 0:
        return profit / risk
    else:
        return profit / width


def ClosePredic(T59, T58, T57):
    T59D1, T59D2 = DerivsCalc(T59, T58, T57)

    ApproxClose = T59 + T59D1 + T59D2

    T00D1, T00D2 = DerivsCalc(ApproxClose, T59, T58)

    SPXClosePredic = T59 + 1 / 2 * (T59D1 + T59D2 + T00D1 + T00D2)
    return SPXClosePredic


def DerivsCalc(T59, T58, T57):
    FirstDeriv = (3 * T59 - 4 * T58 + T57) / 2
    SecondDeriv = (T59 - 2 * T58 + T57)
    return FirstDeriv, SecondDeriv



def runStratWithStopLossTakeProfit(optionSnapshotMap, stratStrikeList, pricesMap, startTime, stopTime, stopLoss, takeProfit, dynamicTP):
    optionLegsList = []
    totalDebit = None
    profit = None

    for strike in stratStrikeList:
        if strike is None:
            print('Strike not found')

        optionLegsList.append(
            [getOptionRowForTimeStrikeType(optionSnapshotMap, startTime, strike[0], strike[1]), strike[2]])

    for optionRow in optionLegsList:
        if optionRow[0] is None:
            return None, None, None, None

    totalCredit = getTotalCostForSpread(optionLegsList, True)

    if dynamicTP:
        takeProfit = -totalCredit * (takeProfit/100)

    nextTime = addMinutesToTimeAsStringReturnString(startTime, 0)
    if stopTime is None:
        while totalCredit is not None:
            nextTime = addMinutesToTimeAsStringReturnString(nextTime, 1)

            if nextTime == '16:00':
                spxClose = float(pricesMap.get('16:00'))
                totalDebit = -calculateOptionMetrics(optionLegsList, spxClose)
                profit = abs(totalCredit) - abs(totalDebit)

                if (takeProfit is None or profit >= takeProfit):
                    profit = takeProfit

                if (stopLoss is None or profit <= stopLoss):
                    profit = stopLoss

                break

            optionLegsList = []

            for strike in stratStrikeList:
                optionLegsList.append(
                    [getOptionRowForTimeStrikeType(optionSnapshotMap, nextTime, strike[0], strike[1]), strike[2]])

            totalDebit = getTotalCostForSpread(optionLegsList, False)

            if totalDebit is None:
                tempStratStrikeList = []
                for strike in optionLegsList:
                    if (strike[1] < 0 and len(strike[0][3]) > 0) or (strike[1] > 0 and len(strike[0][2]) > 0):
                        tempStratStrikeList.append(strike)

                totalDebit = getTotalCostForSpread(tempStratStrikeList, False)

                if totalDebit is None:
                    continue

            profit = abs(totalCredit) - abs(totalDebit)

            if (takeProfit is None or profit >= takeProfit):
                profit = takeProfit
                break

            if (stopLoss is None or profit <= stopLoss):
                profit = stopLoss
                break

            if profit is None:
                continue

        return totalCredit, totalDebit, profit, nextTime
    else:
        totalCredit, totalDebit, optionSpreadPnL, profit = runStratFromStartTimeToStopTime(optionSnapshotMap=optionSnapshotMap, stratStrikeList=stratStrikeList, pricesMap=pricesMap, startTime=startTime, stopTime=stopTime)

        return totalCredit, totalDebit, abs(totalCredit) - abs(totalDebit), stopTime

def runStratFromStartTimeToStopTime(optionSnapshotMap, stratStrikeList, pricesMap, startTime, stopTime):
    optionLegsList = []
    totalDebit = None
    optionSpreadPnL = None

    for strike in stratStrikeList:
        if strike is None:
            print('Strike not found')

        optionLegsList.append(
            [getOptionRowForTimeStrikeType(optionSnapshotMap, startTime, strike[0], strike[1]), strike[2]])

    for optionRow in optionLegsList:
        if optionRow[0] is None:
            return None, None, None, None

    totalCredit = getTotalCostForSpread(optionLegsList, True)

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

            totalDebit = getTotalCostForSpread(optionLegsList, False)

            profit = totalDebit - totalCredit

        return totalCredit, totalDebit, optionSpreadPnL, profit
    else:
        return None, None, None, None

def addMinutesToTimeAsStringReturnString(timeString, minutes):
    startTimedt = datetime.datetime.strptime(timeString, '%H:%M')
    startTimedt = startTimedt + datetime.timedelta(minutes=minutes)

    return datetime.datetime.strftime(startTimedt, '%H:%M')


def generateFullDayOfTimes():
    timeList = []
    run = True
    startTimedt = datetime.datetime.strptime('09:30', '%H:%M')
    while run:
        startTimedt = startTimedt + datetime.timedelta(minutes=1)
        startTimedtStr = datetime.datetime.strftime(startTimedt, '%H:%M')

        if startTimedtStr > '16:00':
            run = False
        else:
            timeList.append(startTimedtStr)

    return timeList


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
        pass
        # print('Cant find file: ' + fileName)

    return optionSnapshotMap


def getExpirationDates(ticker, dateFilter=None, isZeroDte=None):
    expirationDates = []
    tickerDir = 'H:/Tickers/' + ticker + '/'
    for dir in os.listdir(tickerDir):
        if isZeroDte:
            zeroDteExpirationDir = tickerDir + dir + '/0931/' + dir
            if (dateFilter is None or dir > dateFilter) and os.path.isdir(zeroDteExpirationDir):
                expirationDates.append(dir)
        elif isZeroDte is False:
            expirationDates.append(dir)

    return expirationDates


def getTotalCostForSpread(optionLegsList, entry):
    cost = 0.0

    for optionLeg in optionLegsList:
        short = optionLeg[1] < 0
        long = optionLeg[1] > 0
        bid = parseS2F(optionLeg[0][2]) if len(optionLeg[0][2]) > 0 else None
        ask = parseS2F(optionLeg[0][3]) if len(optionLeg[0][3]) > 0 else None
        numberOfContracts = abs(optionLeg[1])

        if entry:
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
        else:
            if short and ask is not None:
                if bid is not None:
                    cost += ((bid + ask) / 2) * numberOfContracts
                else:
                    cost += ask * numberOfContracts
            elif long:
                if ask is not None and bid is not None:
                    cost -= ((bid + ask) / 2) * numberOfContracts
                elif bid is not None:
                    cost -= bid * numberOfContracts
            else:
                # print("Malformed leg: " + str(optionLeg))
                return None

    return cost


def getOptionRowForTimeStrikeType(optionSnapshotMap, time, strike, type):
    """
    Returns the list of the option at a given time, strike, whether or not it is a P/C.

    Extended Summary
    ----------------
    Uses the dictionary to map down into the time and strike prices to find the specific set
    of options and the dictionary returns a list of 2 options. Then we loop over the list to 
    find and return the specific type we're looking for, put or call.

    Parameters
    ----------
    optionSnapshotMap:
        The option snapshot map for the day in dictionary form, can be indexted via
        optionSnapshotMap.get(time).get(str(strike)) 

    time: string
        Time to be evaluated at works in HH:MM time from 9:31 to 16:00

    strike: float
        Strike of the given option

    type: string
        Put/Call represented as "P" or "C"
    
    
    Returns
    -------
    optionRow: list
        Returns a list of the option requestion in the following format:
        [strike, options type, bid, ask, delta, gamma, theta, vega]
    """
    if optionSnapshotMap.get(time) is None:
        print()

    tempList = optionSnapshotMap.get(time).get(str(strike))

    if tempList is not None:
        for optionRow in tempList:
            if optionRow[1] == type:  # P or C
                return optionRow


def calculateOptionMetrics(optionLegsList, closePrice):
    """
    Calculates the profit for the associated strategy depending on the closing price of the underlying.


    Extended Summary
    ----------------
    A given options strategy is made up of a series of legs, each with an associated credit/debit
    and the strategy has an overall location of profitability depending on if the option is shorted
    or longed. This sums the overall profit/loss of the entire list of legs of any arbitrary sized 
    options strategy at close


    Parameters
    ----------
    optionLegList: list
        A list where each row has the following form:
        [strike, options type, bid, ask, delta, gamma, theta, vega]

    closePrice: float
        Closing price of the underlying


    Returns
    -------
    Profit: float
        Profit of the strategy based upon the short/long of options - has nothing to with credit/debits
    """

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


def parseS2F(string):
    """
    Returns the float equivalent of the string from the option's bid/ask, if it exists.

    Extended Summary
    ----------------
    Converts a given string into the equivalent float, if it exists, and if it doesn't it is 
    assumed to be a zero value and instead returns zero as no listed bid/ask would imply it is 0.

    Parameters
    ----------

    string: string
        Input string that contains only numbers

    Returns
    -------
        Returns the numeric equivalent of that string in float form.
    """
    # Non-existant string -> bid/ask is 0
    if len(string) == 0:
        return 0.0
    else:
        return float(string)