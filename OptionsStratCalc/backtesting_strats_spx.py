from ast import Num
from operator import index
import numpy as np
import os
import csv
import math
import datetime as dt

def PCS_SPX(TradeParameters, StartDate, ScalingMethod):
    """Backtests selling M2W, W2F, and F2M put credit spreads on SPX and resulting gains/losses.

    Extended Summary
    ----------------
    Backtests selling credit spreads at market open and letting them run and either buying to close, or letting
    them expire for profit on the S&P500 index, SPX. We make an assumption that the EoD prices are equal to that
    of market open and linearly interpolate in between on the option prices. If we hit our desired debit prices, or
    a stop loss kicks in, then the spread is bought to close and the resulting premium is added to the account balance.
    Taxes and missions as well as other fees are also considered.


    Parameters
    ----------
    TradeParameters : np.array
        [account balance, maximum risk % per trade, delta-value, maximum risk total]

    StartDate : datetime
        Initial starting date of the backtesting period, must be at or after Jan 5, 2016

    ScalingMethod : string
        A string that picks between "width" scaling (larger contract sizes) vs number of "contracts" 


    Returns
    -------
    BacktestResults : np.array
        Array containing the following information:
        [final profit, total number of times traded, total number of spreads traded, ...
        number of trades totally won, number of trades partially won, number of trades partially lost, ...
        number of trades totally lost, amount spent on taxes, amount spent on comissions]
    """
    global SPXHistPrice, SPXPutChain
    global SymCol, BidCol, OfrCol, DelCol, DayCol, ExpCol
    # Load in all our data for testing
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"
    SPXHistPrice = "SPX_daily_prices.csv"
    SPXPutChain = "SPXPutsChain.csv"

    SPXHistPrice = os.path.join(Folder, SPXHistPrice)
    SPXPutChain = os.path.join(Folder, SPXPutChain)

    # Output array
    BacktestResults = np.zeros([9,1])

    # Read in the data files
    with open(SPXHistPrice) as DataFile:
        SPXHistPrice = list(csv.reader(DataFile))
    SPXHistPrice.reverse()

    with open(SPXPutChain) as DataFile:
        SPXPutChain = list(csv.reader(DataFile))
    SPXPutChain.reverse()

    # Grab the needed columns from each data file
    Header = np.array(SPXHistPrice[0])
    OpnCol = int(np.where(Header == "Open")[0])
    ClsCol = int(np.where(Header == "Close/Last")[0])
    HDTCol = int(np.where(Header == "Date")[0])

    Header = np.array(SPXPutChain[0])
    DayCol = int(np.where(Header == "date")[0])
    SymCol = int(np.where(Header == "symbol")[0])
    BidCol = int(np.where(Header == "best_bid")[0])
    OfrCol = int(np.where(Header == "best_offer")[0])
    DelCol = int(np.where(Header == "delta")[0])
    ExpCol = int(np.where(Header == "exdate")[0])

    # Convert for speed
    SPXHistPrice = np.array(SPXHistPrice[1:])
    SPXPutChain = np.array(SPXPutChain[1:])

    # Find the index of the starting date of the trades
    SPXDateOffset = str(StartDate.strftime("%m")) + "/"\
         + str(StartDate.strftime("%d")) + "/" + str(StartDate.strftime("%Y"))

    for i in range(len(SPXHistPrice)):
        if SPXHistPrice[i][HDTCol] == SPXDateOffset: SPXDateOffset = i; break

    # Force our trades to begin on the M2W, W2F, F2M schedule
    if StartDate.strftime("%a") == "Tue" or "Thu" or "Sun":
        SPXDateOffset +=1
    elif StartDate.strftime("%a") == "Sat":
        SPXDateOffset +=2

    ChainDateOffset = 0
    # Find the day in the chain which is our starting day
    ChainDate = str(StartDate.strftime("%Y"))\
         + str(StartDate.strftime("%m")) + str(StartDate.strftime("%d"))
    for i in range(len(SPXPutChain)):
        if SPXPutChain[i][DayCol] == ChainDate: ChainDateOffset = i; break


    # Comissions and fees per opening/closing a spread based off of TastyWorks
    Fees = 3.08

    # Initialize our position and misc parameters
    Position = False
    PrevIndex = 0
    ExpDate = StartDate - dt.timedelta(days=1)
    WidthScaling = 5000

    # Outer loop that goes from start date to Dec 31, 2020
    for iDate in range(SPXDateOffset, len(SPXHistPrice)-1):

        CurrentDay = dt.datetime(int(SPXHistPrice[iDate][HDTCol][6:]), \
            int(SPXHistPrice[iDate][HDTCol][0:2]), \
                int(SPXHistPrice[iDate][HDTCol][3:5]))
        Weekday = CurrentDay.strftime("%a")

        if ScalingMethod == "width":
            if TradeParameters[0] > WidthScaling: Width = 1 + math.floor(1 + TradeParameters[0]/WidthScaling)
            else: Width = 1
        elif ScalingMethod == "contracts": Width = 1

        if TradeParameters[0] < 0:
            print(CurrentDay)
            print("!WARNING! ----- Account is now negative balance, this is your margin call alert. ----- !WARNING!")
            break

        # Define out maximum risk for this trade cycle
        MaxRisk =  TradeParameters[0] * TradeParameters[1]
        if MaxRisk > TradeParameters[3]: MaxRisk = TradeParameters[3]
        
        # Close price of SPX and make out intraday array
        SPXC = float(SPXHistPrice[iDate][ClsCol])
        SPXO = float(SPXHistPrice[iDate][OpnCol])

        # Check the closing price and compare it to our break evens - see what our resulting profit is
        if CurrentDay == ExpDate and Position:

            # Condition 1 - Full win with SPX closing above the short strike
            if SPXC > Strike:
                # Calculate the total profit of the trade
                Profit =  Credit * NumberSpreads - TotalFees
                BacktestResults[3] +=1

            # Condition 2 - Partial win with SPX closing above breakeven
            elif SPXC < Strike and SPXC > Breakeven:
                # Calculate the total profit of the trade
                Profit = (Credit - (Strike - SPXC)) * NumberSpreads - TotalFees
                BacktestResults[4] +=1

            # Condition 3 - Partial loss with SPX closing below breakeven but above long strike
            elif (SPXC < Breakeven and SPXC > (Strike - Width)) or (SPXC < (Strike - Width)):
                # Assume that with reasonable monitoring we can buy to close at 2.5x credit
                Profit =  (Credit -  2.5*Credit) * NumberSpreads - TotalFees
                BacktestResults[5] +=1

            #     # Calculate the total profit of the trade
            #     Profit = (Credit - (Strike - SPXC)) * NumberSpreads - TotalFees
            #     BacktestResults[5] +=1

            # # Condition 4 - Total loss with SPX closing below the long strike
            # elif SPXC < (Strike - Width):
            #     # Calculate the total profit of the trade
            #     Profit = -Risk * NumberSpreads - TotalFees
            #     S1 = "On " + str(CurrentDay.year) + "-" + str(CurrentDay.month) + "-" + str(CurrentDay.day)
            #     S2 = " we had a total loss because SPY traded at: $" + str(SPXC)
            #     S3 = " and our long-put was at a strike of $" + str(int(Strike-Width))
            #     S4 = " and we lost $" + str(int(NumberSpreads * Risk))
            #     print(S1 +  S2 + S3 + S4)
            #     BacktestResults[6] +=1

            # Calculate the amount of taxes to be paid
            if Profit > 0: Taxes = Profit * 0.2
            else: Taxes = 0
            
            # Add to our account balances
            TradeParameters[0] += Profit - Taxes
            BacktestResults[0] += Profit - Taxes
            BacktestResults[7] += Taxes

            # Update our position
            Position = False

        if (Weekday == "Mon" or Weekday == "Wed") and not Position:
            DTE = 2
            Credit, Risk, Strike, Position, PrevIndex, ExpDate = \
                OpenPCSSPX(TradeParameters[2], Width, SPXHistPrice[iDate][HDTCol], PrevIndex, DTE, CurrentDay)
            if Risk == 0: continue # No risk -> trade not available so skip it and continue to next cycle

            # Break even price 
            Breakeven =  Strike - Credit/100

            # Calculate number of spreads and fees to be paid
            NumberSpreads = (MaxRisk / Risk)
            if NumberSpreads < 1: NumberSpreads = 1
            else: NumberSpreads = math.floor(NumberSpreads)

            TotalFees = NumberSpreads * Fees

            # Add to our results array
            BacktestResults[1] += 1
            BacktestResults[2] += TotalFees

        elif (Weekday == "Fri") and not Position:
            DTE = 3
            Credit, Risk, Strike, Position, PrevIndex, ExpDate = \
                OpenPCSSPX(TradeParameters[2], Width, SPXHistPrice[iDate][HDTCol], PrevIndex, DTE, CurrentDay)
            if Risk == 0: continue # No risk -> trade not available so skip it and continue to next cycle
            
            # Break even price 
            Breakeven =  Strike - Credit/100
            
            # Calculate number of spreads and fees to be paid
            NumberSpreads = (MaxRisk / Risk)
            if NumberSpreads < 1: NumberSpreads = 1
            else: NumberSpreads = math.floor(NumberSpreads)

            TotalFees = NumberSpreads * Fees

            BacktestResults[1] += 1 # add to times traded
            BacktestResults[2] += NumberSpreads # add to number of spreads traded
            BacktestResults[8] += TotalFees # add to amount paid in comissions
        
    return BacktestResults

def OpenPCSSPX(Delta, Width, Date, IndexOffset, DTE, Day):
    """Calculates value for selling a PCS on SPX for a given delta on that date.

    Extended Summary
    ----------------
    Finds the credit and risk assigned for selling a PCS on SPX for a given delta using a given width
    as our long/insurance position .


    Parameters
    ----------
    Delta : float
        Delta the short put is at

    Width : int
        How many strikes down the long put is at

    Date : string
        The current date which is used to evaluate the put chain

    IndexOffset : int
        Starting point for loop, speeds up look up times

    Day : datetime
        The day the trade was initialized


    Returns
    -------
    Credit : float
        Credit received for the PCS

    Risk : float
        Amount of money used as collateral for the PCS

    StrikeP : int
        Strike of the short and long puts for the PCS

    Active : boolean
        Updates the position to be true

    Index : int
        New index for looping when checking value of the spread
    """
    if (Day.strftime("%a") == "Mon"):
        DatePrevClose = Day - dt.timedelta(days=3)
    elif (Day.strftime("%a") == "Tue" or "Wed" or "Thur" or "Fri"):
        DatePrevClose = Day - dt.timedelta(days=1)

    DatePrevClose = DatePrevClose.strftime("%Y") + DatePrevClose.strftime("%m") + DatePrevClose.strftime("%d")
    ExpDate = Day + dt.timedelta(days=DTE)
    ExpDateS = ExpDate.strftime("%Y") + ExpDate.strftime("%m") + ExpDate.strftime("%d")

    for i in range(IndexOffset, len(SPXPutChain)):
        if SPXPutChain[i][DayCol] == DatePrevClose and SPXPutChain[i][ExpCol] == ExpDateS and\
              abs(float(SPXPutChain[i][DelCol])) > Delta:
            break
        # We've gone too far forward in time/the list and we can just exit it
        # Date = dt.datetime(int(SPXPutChain[i][DayCol][0:4]), int(SPXPutChain[i][DayCol][4:6]), int(SPXPutChain[i][DayCol][6:]))
        if i > (len(SPXPutChain)-1000) and not (SPXPutChain[i][DayCol] == DatePrevClose): 
            Credit = 0; Risk = 0; ShortPutStrike = 0; Active = 0; Index = IndexOffset; ExpDate = 0
            return Credit, Risk, ShortPutStrike, Active, Index, ExpDate

    PIndex = SPXPutChain[i][SymCol][6:].find("P")
    ShortPutStrike = int(SPXPutChain[i][SymCol][6+PIndex+1:6+PIndex+5])
    ShortPrice = (float(SPXPutChain[i][BidCol]) + float(SPXPutChain[i][OfrCol]))/2
    LongPrice = (float(SPXPutChain[i-Width][BidCol]) + float(SPXPutChain[i-Width][OfrCol]))/2

    Credit = abs(round((ShortPrice - LongPrice)*100, 2))
    Risk = (500 * Width) - Credit
    Active =  True
    Index = i

    return Credit, Risk, ShortPutStrike, Active, Index, ExpDate

def FetchPrice(Date, Strike, Expiration, LastIndex):
    """Finds the value of that specific SPX option on that given day - assuming it exists.

    Extended Summary
    ----------------
    Finds the price in dollars for the value of the SPX option on that given day. Uses the date,
    the strike, and the expiration date in order to sift through the historical chain and find the same
    option on the new date. The LastIndex gives us a better starting point so we don't have to run through
    the entire array.


    Parameters
    ----------
    Date : datetime
        The day that we're looking up the option on

    Strike : int
        Strike price of SPX

    Expiration : datetime
        The day that the contract expires on

    LastIndex : int
        Starting point for loop, speeds up look up times


    Returns
    -------
    Price : float
        Returns the price of the contract in dollars
    """
    DateS = Date.strftime("%Y") + Date.strftime("%m") + Date.strftime("%d")
    EDateS = Expiration.strftime("%Y") + Expiration.strftime("%m") + Expiration.strftime("%d")
    StrikeS = str(Strike)

    for i in range(LastIndex, len(SPXPutChain)):
        if SPXPutChain[i][DayCol] == DateS and SPXPutChain[i][ExpCol] == EDateS\
             and (StrikeS in SPXPutChain[i][SymCol]): break
    Price = (float(SPXPutChain[i][BidCol]) + float(SPXPutChain[i][OfrCol]))/2
    
    return Price * 100