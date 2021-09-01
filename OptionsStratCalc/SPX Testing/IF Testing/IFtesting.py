import concurrent.futures
import csv
import datetime
import math
import os.path
import time


def SPX_SL_TP_Multi():
    """Runs the SPX strategy with a stop-loss or price-target in multi-threading.

    Extended Summary
    ----------------
    Runs a generic SPX strategy developed in SPX_SL_SP that is able to run for a specific
    price target and/or stop loss. This "runner" function runs the strategy in a multi-threaded
    form in order to speed up the processing time.

    Returns
    -------
    resultsMain : list
        Produces a list in the format specified by SPX_SL_SP that can be written to a data file,
        or manipulated for visualization
    """
    resultsMain = []
    allExpiration = getExpirationDates(ticker='SPXW', isZeroDte=True)

    multi = True

    if multi:
        with concurrent.futures.ProcessPoolExecutor(4) as executor:
            resultsMain = list(executor.map(SPX_SL_TP, allExpiration))
    else:
        for expiration in allExpiration:
            print(expiration)
            resultsMain.append(SPX_SL_TP(expiration))

    #print(resultsMain)
    return resultsMain


def SPX_SL_TP(expiration):
    """Runs the SPX strategy for the given expiration date

    Parameters
    ----------
    expiration : [type]
        [description]

    Returns
    -------
    results : list
        List of data that's a list of the specified results for the strategy. 
        Has the following form:
        []

    """
    print(expiration)
    ticker = 'SPXW'
    startTime = '09:31'
    stopTime = '11:00'
    # Width of the IF
    width = 25
    start = '2016-09-01'
    end = '2016-09-02'
    dynamicTP = False

    timeList = ['09:31', '09:45', '10:00']

    #while '12:00' not in timeList:
    #    timeList.append(addMinutesToTimeAsStringReturnString(timeList[-1], 15))

    widthStart = 10
    widthMax = 50
    widthIncrement = 5

    widthList = []

    for i in range(widthStart, widthMax - 1, widthIncrement):
        widthList.append(i)

    stopLossStart = -1
    stopLossStop = -3
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
        takeProfitStart = 1
        takeProfitStop = 3
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
        for t in timeList:

            tempMap = makeOptionSnapshotMapFromShortType(rootFilter=ticker, dateFilter=expiration,
                                                        timeFilter=startTime, expirationFilter=expiration)

            optionSnapshotMap.update({t: tempMap})

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
    rootDirectory = 'C:/Users/Admin/Downloads/'
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
    """Uses numerical integration to approximate the closing price of SPX on a given day.

    Extended Summary
    ----------------
    Uses a Predictor-Corrector method and the last 3 minutes' prices at the 15:XX:00 mark
    to predict what SPX is going to close at. 

    Parameters
    ----------
    T59 : float
        Price of SPX at 15:59:00 on the given day
        
        
    T58 : float
        Price of SPX at 15:58:00 on the given day

    T57 : float
        Price of SPX at 15:58:00 on the given day


    Returns
    -------
    SPXClosePredic : float
        The predicted closing price of SPX
    """
    T59D1, T59D2 = DerivsCalc(T59, T58, T57)

    ApproxClose = T59 + T59D1 + T59D2

    T00D1, T00D2 = DerivsCalc(ApproxClose, T59, T58)

    SPXClosePredic = T59 + 1 / 2 * (T59D1 + T59D2 + T00D1 + T00D2)
    return SPXClosePredic


def DerivsCalc(Nought, Nought1, Nought2):
    """
    Calculates the numerical derivatives from the 3 given data points.

    Extended Summary
    ----------------
    Calculates the numerical first and second derivatives for at point
    nought using the two time steps previous in time, nought-deltaT (Nought1),
    and nought-2deltaT (Nought2). The two schemes used are left-sided second order
    accurate for the first derivative, and second order central first order accurate
    for the second derivative.

    Parameters
    ----------
    Nought: float
        The point at which you want to take derivatives at

    Nought1: float
        One time-step back in time from the point nought (Nought - deltaT)

    Nought2: float
        Two time-steps back in time from the point nought (Nought - 2*deltaT)

    Returns
    -------
    FirstDeriv: float
        First derivative at the point nought

    SecondDeriv: float
        Second derivative at the point nought

    
    
    """
    # First derivative, second order, Left-Sided Difference Scheme
    FirstDeriv = (3 * Nought - 4 * Nought1 + Nought2) / 2
    # Second Derivative, First Order, Central Difference scheme
    SecondDeriv = (Nought - 2 * Nought1 + Nought2)
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
    rootDirectory = 'C:/Users/Admin/Downloads/'
    optionSnapshotMap = {}
    if int(timeFilter[0]) == 9:
        fileName = rootDirectory + rootFilter + '/' + dateFilter + '/' + timeFilter.replace('9:', '09') + '/' + \
            expirationFilter + '/' + 'ShortUnderlyingOptionsIntervals_60sec_calcs_oi_level2_' + dateFilter + '.csv'
    else:
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
    tickerDir = 'C:/Users/Admin/Downloads/' + ticker + '/'
    for dir in os.listdir(tickerDir):
        if isZeroDte:
            zeroDteExpirationDir = tickerDir + dir + '/0931/' + dir
            if (dateFilter is None or dir > dateFilter) and os.path.isdir(zeroDteExpirationDir):
                expirationDates.append(dir)
        elif isZeroDte is False:
            expirationDates.append(dir)

    return expirationDates


def getTotalCostForSpread(optionLegsList, entry):
    """[summary]

    Parameters
    ----------
    optionLegsList : list
        List of options and their respective legs in the following format
        [strike, options type, bid, ask, delta, gamma, theta, vega]
        [description]
    entry : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """
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
    # If our map returns empty for that time, print something
    if optionSnapshotMap.get(time) is None:
        print("Map is fucked")

    # Grab the list for that strike and time
    tempList = optionSnapshotMap.get(time).get(str(strike))

    # Return the associated P/C at that strike, at that time in the following format
    # [strike, options type, bid, ask, delta, gamma, theta, vega]
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
        "Profit of the strategy based upon the short/long of options, it
        has nothing to with credit/debits. This is like for P&L diagrams
        or something" - George (paraphrased by Erik)
    """

    profit = 0

    # Looping over the legs in the stategy to find the P&L for the cash settlements
    for optionLeg in optionLegsList:
        strike = parseS2F(optionLeg[0][0])

        put = optionLeg[0][1] == 'P'

        call = optionLeg[0][1] == 'C'
        short = optionLeg[1] < 0
        long = optionLeg[1] > 0
        numberOfContracts = abs(optionLeg[1])

        # Short puts have negative profit if we close below the strike
        if put and short:
            if closePrice < strike:
                profit += (closePrice - strike) * numberOfContracts
        # Long puts have positive profit if we close below the strike
        elif put and long:
            if closePrice < strike:
                profit += (strike - closePrice) * numberOfContracts
        # Short calls have negative profit if we close above the strike
        elif call and short:
            if closePrice > strike:
                profit += (strike - closePrice) * numberOfContracts
        # Long calls have positive profit if we close above the strike
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
    # zeroDTEs = getExpirationDates(ticker='SPXW', isZeroDte=True)

    # with concurrent.futures.ThreadPoolExecutor(24) as executor:
    #    resultsMain = list(executor.map(SPX_M2W_G, zeroDTEs))
    resultsMain = []
    # strats = ['IFDM2W', 'IFUM2W', 'IFCM2W', 'IFPM2W', 'DoubleIFM2W', 'ICM2W']
    # for strat in strats:
    #   print(strat)
    #    for zeroDTE in zeroDTEs:
    #       resultsMain.append(SPX_M2W_G2(strat=strat, width=5, date=zeroDTE, size=1, startTime='15:59', stopTime=None))

    # for zeroDTE in zeroDTEs:
    #    resultsMain.append(SPX_M2W_G(zeroDTE))

    resultsMain = SPX_SL_TP_Multi()

    totalMapTime = time.time() - start2
    print(totalMapTime)

    # SPX_M2W_G('2016-09-02')

    # with concurrent.futures.ProcessPoolExecutor(12) as executor:
    #   resultsMain = list(executor.map(SPX_M2W, filenamesFiltered))

    resultsFinal = []
    for result in resultsMain:
        if result is not None:
            for r in result:
                if r is not None:
                    resultsFinal.append(r)

    with open("output.csv", "w", newline="\n") as f:
        writer = csv.writer(f)
        headers = ['Date', 'Trade Type', 'P/L', 'Credit', 'Risk', 'Total Debit', 'Start Time Spot', 'Stop Time Spot',
                   'Stop Time', 'Return', 'Positive Return', 'Negative Return']

        #headers = ['Date', 'Trade Type', '9:31 Abs Daily Move <= Implied Move',
         #          '9:32 Abs Daily Move <= Implied Move',
          #         '9:33 Abs Daily Move <= Implied Move',
           #        '9:34 Abs Daily Move <= Implied Move',
            #       '9:35 Abs Daily Move <= Implied Move',
             #      '15:55 Abs Daily Move <= Implied Move',
              #     '15:56 Abs Daily Move <= Implied Move',
               #    '15:57 Abs Daily Move <= Implied Move',
                #   '15:58 Abs Daily Move <= Implied Move',
                 #  '15:59 Abs Daily Move <= Implied Move']

        # timeList = []
        # startTimedt = datetime.datetime.strptime('09:35', '%H:%M')
        # run = True
        # while run:
        #   startTimedt = startTimedt + datetime.timedelta(minutes=5)
        #  startTimedtStr = datetime.datetime.strftime(startTimedt, '%H:%M')

        # if startTimedtStr > '16:00':
        #    run = False
        # else:
        #   timeList.append(startTimedtStr)

        #differenceInSize = int((len(max(resultsFinal, key=len)) - len(headers)) / 3)
        #for i in differenceInSize:#timeList:
        #    headers.append('Strike ' + str(i))
        #    headers.append('Strike ' + str(i) + ' Option Type')
        #    headers.append('Strike ' + str(i) + ' Size')
        # '{time} Implied Move', 'Abs {time} Spot - Close', '{time} Abs Difference'
        #   headers.append('{time} Abs Daily Move <= Implied Move'.replace('{time}', i))

        writer.writerows([headers])
        writer.writerows(resultsFinal)

    # print(results)


if __name__ == '__main__':
    main()
