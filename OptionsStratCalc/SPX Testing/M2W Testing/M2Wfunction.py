import csv
import math
import datetime as dt
import numpy as np

def SPX_M2W(Filename):
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
    Date = Filename[len(Filename)-5:len(Filename)-15:-1]
    # Date is in YYYY-MM-DD format
    ExpDate = Date[::-1]
    Date = Date[::-1]

    # Check to see if M/W/F, skip to next day if we're not M/W/F, also skipping market holidays
    Date = dt.datetime(int(Date[0:4]), int(Date[5:7]), int(Date[8::]))
    if Date.strftime("%a") == "Tue" or Date.strftime("%a") == "Thu":
        FullList = [[None for _ in range(16)] for _ in range(3)]
        return FullList

    # Load in data, reverse and find index of 15:57 EST, all the information we need exists between close
    # and after 15:57 EST
    with open(Filename) as DailyData:
        DailyChain = list(csv.reader(DailyData))
    DailyChain.reverse()

    MaxIndex = len(DailyChain)
    for i in range(1, len(DailyChain)):
        if DailyChain[i][0] == "15:57":
            MaxIndex = i
            break
    
    # Find spot price at 15:59 EST
    Spot = 0
    for i in range(1, MaxIndex):
        if DailyChain[i][0] == "15:59":
            Spot = float(DailyChain[i][6])
            break


    # --- NOTE FOR GEO ---
    # Other 2 functions are WIP, I want to see if this first one works
    # and if it does I can have the other 2 done by EOD 7/20/21

    # WriteIC(DailyChain, Spot, MaxIndex, ExpDate)
    IFUList = WriteIFU(DailyChain, Spot, MaxIndex, ExpDate)
    # WriteIFD(DailyChain, Spot, MaxIndex, ExpDate)

    FullList = IFUList
    return FullList

def WriteIFU(OptionsChain, Spot, MaxIndex, ExpDate):
    """Runs a M2W IF on SPX at the closest strike above the spot price of SPX at 15:59 EST,
    and writes results to a CSV file. 

    Extended Summary
    ----------------
    Records various parameters on a given 0DTE day for what the possible returns and parameters for those
    returns would be for a M2W IF trade placed at 15:59 PM EST. Information regarding each trade is then
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

    ExpDate: string
        Date of expiration in "YYYY-MM-DD" format

    Returns
    -------
    TradeInformation: list
        List of the following information:
        [date, trade type (IF/IC), P/L, Credit, Risk, Spot@15:58, Spot@15:59, Spot@16:00, short call strike, ...
         long call strike, short put strike, long put strike, check 1, difference to short put, ...
         difference to short call, "momentum"]
    """
    # Strikes for the M2W IF using the closest strike above where SPX is trading
    ShortStrike = math.ceil(Spot / 5) * 5
    LongCall = ShortStrike + 5
    LongPut = ShortStrike - 5

    PreviousSpot = 0
    SPXClose = 0
    ShortPutCredit = 0
    ShortCallCredit = 0
    LongPutDebit = 0
    LongCallDebit = 0

    # Grab the four legs of the trade & the closing price (spot at 16:00 EST)
    for i in range(1, MaxIndex):
        if OptionsChain[i][0] == "15:58": PreviousSpot = float(OptionsChain[i][6])
        if OptionsChain[i][0] == "16:00": SPXClose = float(OptionsChain[i][6])
        if OptionsChain[i][0] == "15:59" and OptionsChain[i][1] == ExpDate and\
            OptionsChain[i][2] == str(ShortStrike) and OptionsChain[i][3] == "P":
                ShortPutCredit =  (float(OptionsChain[i][4]) + float(OptionsChain[i][5])) / 2
        if OptionsChain[i][0] == "15:59" and OptionsChain[i][1] == ExpDate and\
            OptionsChain[i][2] == str(ShortStrike) and OptionsChain[i][3] == "C":
                ShortCallCredit =  (float(OptionsChain[i][4]) + float(OptionsChain[i][5])) / 2
        if OptionsChain[i][0] == "15:59" and OptionsChain[i][1] == ExpDate and\
            OptionsChain[i][2] == str(LongPut) and OptionsChain[i][3] == "P":
                LongPutDebit =  (float(OptionsChain[i][4]) + float(OptionsChain[i][5])) / 2
        if OptionsChain[i][0] == "15:59" and OptionsChain[i][1] == ExpDate and\
            OptionsChain[i][2] == str(LongCall) and OptionsChain[i][3] == "C":
                LongCallDebit =  (float(OptionsChain[i][4]) + float(OptionsChain[i][5])) / 2

    # Find the total amount of credit for the IF as well as the risk
    TotalCredit = ShortPutCredit + ShortCallCredit - LongPutDebit - LongCallDebit
    Risk = 5 - TotalCredit

    # Break evens
    UpperBE = ShortStrike + TotalCredit
    LowerBE = ShortStrike - TotalCredit

    # 3 Conditions - Profit, Partial Loss, Max Loss

    Profit = 0
    # Condition 1 - Check if we're in the breakeven zone for profit
    if SPXClose < UpperBE and SPXClose > LowerBE:
        Profit  = TotalCredit - abs(SPXClose - ShortStrike)
    
    # Condition 2 - Partial loss if we're between longs and BE's
    elif (SPXClose > LongPut and SPXClose < LowerBE) or\
         (SPXClose < LongCall and SPXClose > UpperBE):
            Profit  = TotalCredit - abs(SPXClose - ShortStrike)

    # Condition 3 - Maximum loss if we're above/below the longs
    elif SPXClose > UpperBE or SPXClose < LowerBE:
        Profit = Risk - TotalCredit

    Profit = round(Profit, 2)

    # Parameter checks - difference to strike & "momentum"
    
    # Parameter 1: abs(Spot - Strike) < $1.50
    if abs(Spot - ShortStrike) < 1.50: P1 = 1
    else: P1 = 0
    Diff2StrikeP = round(ShortStrike - Spot, 2)
    Diff2StrikeC = round(ShortStrike - Spot, 2)

    # Parameter 2: (Spot - Spot @ 15:58)
    P2 = PreviousSpot - Spot

    TradeInformation = [ExpDate, "IF", Profit, TotalCredit, Risk, PreviousSpot, Spot, SPXClose,\
        ShortStrike, LongCall, ShortStrike, LongPut, P1, Diff2StrikeC, Diff2StrikeP, P2]

    return TradeInformation

def WriteIFD(OptionsChain, Spot, MaxIndex, ExpDate):
    """Runs a M2W IF on SPX at the closest strike below the spot price of SPX at 15:59 EST,
    and writes results to a CSV file. 
    
    Extended Summary
    ----------------
    Records various parameters on a given 0DTE day for what the possible returns and parameters for those
    returns would be for a M2W IF trade placed at 15:59 PM EST. Information regarding each trade is then
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



    return

def WriteIC(OptionsChain, Spot, MaxIndex, ExpDate):
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



    return


