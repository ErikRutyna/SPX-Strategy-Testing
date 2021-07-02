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
        number of trades totally lost, amount spent on taxes, amount spent on comissions, ...
        average return on collateral]
    """
    global SPXHistPrice, SPXPutChain
    global SymCol, BidCol, OfrCol, DelCol, DayCol, ExpCol

    # Load in all our data for testing
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"
    SPXHistPrice = "SPX_daily_prices.csv"
    SPXPutChain = "Puts.csv"

    # Full file path
    SPXHistPrice = os.path.join(Folder, SPXHistPrice)
    SPXPutChain = os.path.join(Folder, SPXPutChain)

    # Output information
    BacktestResults = np.zeros([10,1])
    ReturnOnCollateral = np.empty([0])

    # Read in the data files
    with open(SPXHistPrice) as DataFile:
        SPXHistPrice = list(csv.reader(DataFile))

    with open(SPXPutChain) as DataFile:
        SPXPutChain = list(csv.reader(DataFile))

    # Grab the needed columns from each data file
    Header = np.array(SPXHistPrice[0])
    # OpnCol = int(np.where(Header == "Open")[0])
    ClsCol = int(np.where(Header == "close")[0])
    HDTCol = int(np.where(Header == "date")[0])

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
    SPXDateOffset = str(StartDate.strftime("%Y")) + \
        str(StartDate.strftime("%m")) + str(StartDate.strftime("%d"))

    for i in range(len(SPXHistPrice)):
        if SPXHistPrice[i][HDTCol] == SPXDateOffset: SPXDateOffset = i; break

    # Force our trades to begin on the M2W, W2F, F2M schedule
    if StartDate.strftime("%a") == "Tue" or "Thu" or "Sun":
        SPXDateOffset +=1
    elif StartDate.strftime("%a") == "Sat":
        SPXDateOffset +=2

    # Comissions and fees per opening/closing a spread based off of TastyWorks
    Fees = 2.54

    # Initialize our position and misc parameters
    Position = False
    PrevIndex = 0
    ExpDate = StartDate - dt.timedelta(days=1)
    WidthScaling = 5000

    # Outer loop that goes from start date to Dec 31, 2020
    for iDate in range(SPXDateOffset, len(SPXHistPrice)-1):

        CurrentDay = dt.datetime(int(SPXHistPrice[iDate][HDTCol][0:4]), \
            int(SPXHistPrice[iDate][HDTCol][4:6]), \
                int(SPXHistPrice[iDate][HDTCol][6:]))
        Weekday = CurrentDay.strftime("%a")

        if ScalingMethod == "width":
            if TradeParameters[0] > WidthScaling: 
                Width = 1 + math.floor(TradeParameters[0]/WidthScaling)
                if Width > 10: Width = 10
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
        # SPXO = float(SPXHistPrice[iDate][OpnCol])

        # Check the closing price and compare it to our break evens - see what our resulting profit is
        if CurrentDay == ExpDate and Position:
            
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
            elif (SPXC < Breakeven and SPXC > (Strike - 5*Width)) or (SPXC < (Strike - 5*Width)):
                # Assume that with reasonable monitoring we can buy to close at 2.5x credit so
                # no such thing as a full loss, only partial losses
                Profit =  (Credit -  2.5*Credit) * NumberSpreads - TotalFees
                BacktestResults[5] +=1

            #     # Calculate the total profit of the trade
            #     Profit = (Credit - (Strike - SPXC)) * NumberSpreads - TotalFees
            #     BacktestResults[5] +=1

            # # Condition 4 - Total loss with SPX closing below the long strike
            # elif SPXC < (Strike - 5*Width):
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

            # Add the % return on collateral
            ReturnOnCollateral = np.append(ReturnOnCollateral, (Profit - TotalFees - Taxes)/Risk * 100)

            # Update our position
            Position = False

        if (Weekday == "Mon" or Weekday == "Wed") and not Position:
            DTE = 2
            Credit, Risk, Strike, Position, PrevIndex, ExpDate = \
                OpenPCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay)
            if Risk == 0: continue # No risk -> trade not available so skip it and continue to next cycle

        elif (Weekday == "Fri") and not Position:
            DTE = 3
            Credit, Risk, Strike, Position, PrevIndex, ExpDate = \
                OpenPCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay)
            if Risk == 0: continue # No risk -> trade not available so skip it and continue to next cycle
        
    BacktestResults[9] = np.mean(ReturnOnCollateral)
    return BacktestResults

def CCS_SPX(TradeParameters, StartDate, ScalingMethod):
    """Backtests selling M2W, W2F, and F2M call credit spreads on SPX and resulting gains/losses.

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
        number of trades totally lost, amount spent on taxes, amount spent on comissions, ...
        average return on collateral]
    """
    global SPXHistPrice, SPXCallsChain
    global SymCol, BidCol, OfrCol, DelCol, DayCol, ExpCol
    # Load in all our data for testing
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"

    SPXHistPrice = "SPX_daily_prices_rev.csv"
    SPXCallsChain = "SPXCallsChain.csv"

    SPXHistPrice = os.path.join(Folder, SPXHistPrice)
    SPXCallsChain = os.path.join(Folder, SPXCallsChain)

    # Output array
    BacktestResults = np.zeros([10,1])
    ReturnOnCollateral = np.empty([0])

    # Read in the data files
    with open(SPXHistPrice) as DataFile:
        SPXHistPrice = list(csv.reader(DataFile))

    with open(SPXCallsChain) as DataFile:
        SPXCallsChain = list(csv.reader(DataFile))

    # Grab the needed columns from each data file
    Header = np.array(SPXHistPrice[0])
    # OpnCol = int(np.where(Header == "Open")[0])
    ClsCol = int(np.where(Header == "Close/Last")[0])
    HDTCol = int(np.where(Header == "Date")[0])

    Header = np.array(SPXCallsChain[0])
    DayCol = int(np.where(Header == "date")[0])
    SymCol = int(np.where(Header == "symbol")[0])
    BidCol = int(np.where(Header == "best_bid")[0])
    OfrCol = int(np.where(Header == "best_offer")[0])
    DelCol = int(np.where(Header == "delta")[0])
    ExpCol = int(np.where(Header == "exdate")[0])

    # Convert for speed
    SPXHistPrice = np.array(SPXHistPrice[1:])
    SPXCallsChain = np.array(SPXCallsChain[1:])

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

    # ChainDateOffset = 0
    # # Find the day in the chain which is our starting day
    # ChainDate = str(StartDate.strftime("%Y"))\
    #      + str(StartDate.strftime("%m")) + str(StartDate.strftime("%d"))
    # for i in range(len(SPXPutChain)):
    #     if SPXPutChain[i][DayCol] == ChainDate: ChainDateOffset = i; break


    # Comissions and fees per opening/closing a spread based off of TastyWorks
    Fees = 2.54

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
        # SPXO = float(SPXHistPrice[iDate][OpnCol])

        # Check the closing price and compare it to our break evens - see what our resulting profit is
        if CurrentDay == ExpDate and Position:
            
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


            # Condition 1 - Full win with SPX closing above the short strike
            if SPXC < Strike:
                # Calculate the total profit of the trade
                Profit =  Credit * NumberSpreads - TotalFees
                BacktestResults[3] +=1

            # Condition 2 - Partial win with SPX closing above breakeven
            elif SPXC > Strike and SPXC < Breakeven:
                # Calculate the total profit of the trade
                Profit = (Credit - (Strike - SPXC)) * NumberSpreads - TotalFees
                BacktestResults[4] +=1

            # Condition 3 - Partial loss with SPX closing below breakeven but above long strike
            elif (SPXC > Breakeven and SPXC < (Strike + 5*Width)) or (SPXC > (Strike + 5*Width)):
                # Assume that with reasonable monitoring we can buy to close at 2.5x credit
                Profit =  (Credit -  2.5*Credit) * NumberSpreads - TotalFees
                BacktestResults[5] +=1

            #     # Calculate the total profit of the trade
            #     Profit = (Credit - (Strike - SPXC)) * NumberSpreads - TotalFees
            #     BacktestResults[5] +=1

            # # Condition 4 - Total loss with SPX closing below the long strike
            # elif (SPXC > (Strike + 5*Width)):
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

            # Add the % return on collateral
            ReturnOnCollateral = np.append(ReturnOnCollateral, (Profit - TotalFees - Taxes)/Risk * 100)

            # Update our position
            Position = False

        if (Weekday == "Mon" or Weekday == "Wed") and not Position:
            DTE = 2
            Credit, Risk, Strike, Position, PrevIndex, ExpDate = \
                OpenCCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay)
            if Risk == 0: continue # No risk -> trade not available so skip it and continue to next cycle

        elif (Weekday == "Fri") and not Position:
            DTE = 3
            Credit, Risk, Strike, Position, PrevIndex, ExpDate = \
                OpenCCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay)
            if Risk == 0: continue # No risk -> trade not available so skip it and continue to next cycle
        
    BacktestResults[9] = np.mean(ReturnOnCollateral)
    return BacktestResults


def OpenPCSSPX(Delta, Width, IndexOffset, DTE, Day):
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

    # String format for date of previous close
    DatePrevCloseS = DatePrevClose.strftime("%Y") + DatePrevClose.strftime("%m") + DatePrevClose.strftime("%d")

    ExpDate = Day + dt.timedelta(days=DTE)
    # String format for our expiration date
    ExpDateS = ExpDate.strftime("%Y") + ExpDate.strftime("%m") + ExpDate.strftime("%d")

    # Define the variables used to find closest to our delta trade
    DeltaDiff = 1
    MinDelta = 1000


    for i in range(IndexOffset, len(SPXPutChain)):
        # This will find the short put that is closest to the delta that we want,
        # and will exit the loop if that option DNE
        if SPXPutChain[i][DayCol] == DatePrevCloseS and SPXPutChain[i][ExpCol] == ExpDateS and\
            abs(float(SPXPutChain[i][DelCol])) < (Delta * 1.5) and \
            abs(float(SPXPutChain[i][DelCol])) > (Delta * 0.66): 
            # Grab the delta of this contract in the loop, find the difference to our set delta
            OptDelta = float(SPXPutChain[i][DelCol])
            DeltaDiff = abs(abs(OptDelta) -  Delta)
            # If a new smaller delta difference is found, update it and record that row
            if DeltaDiff < MinDelta:
                MinDelta = DeltaDiff
                iMinDelta = i
        # Exit function early if we cannot find a short put that matches the criteria
        elif (SPXPutChain[i][DayCol] == ExpDateS or i == (len(SPXPutChain)-1)): break
    # If we have too big of a variance, it means we cannot find a spread to fit our criteria and
    # just need to skip this trade cycle
    if MinDelta > 0.5:
        Credit = 0; Risk = 0; ShortPutStrike = 0; Active = 0; Index = IndexOffset; ExpDate = 0
        return Credit, Risk, ShortPutStrike, Active, Index, ExpDate

    # Need to know string information for the symbol column to find the strike
    PIndex = SPXPutChain[iMinDelta][SymCol][6:].find("P")
    ShortPutStrike = int(SPXPutChain[iMinDelta][SymCol][6+PIndex+1:6+PIndex+5])

    # Grab the price of our short position
    ShortPrice = (float(SPXPutChain[iMinDelta][BidCol]) + float(SPXPutChain[iMinDelta][OfrCol]))/2
    # ShortPutSymbol = SPXPutChain[i][SymCol]

    # Rebuild the symbol for our long position
    LongPutSymbol = ShortPutStrike - Width*5
    LongPutSymbol = str(LongPutSymbol)
    LongPutSymbol = "SPXW " + ExpDate.strftime("%y") + ExpDate.strftime("%m")\
         + ExpDate.strftime("%d") + "P" + LongPutSymbol + "000"
    
    # Loop back over the chain and look for the long put's symbol
    for iLong in range(IndexOffset, len(SPXPutChain)):
        if SPXPutChain[iLong][SymCol] == LongPutSymbol and SPXPutChain[iLong][DayCol] == DatePrevCloseS: break
    # If we can't find the appropriate long put contract, assume credit is ~10% of the width
    if iLong >= 1716210: Credit = 0.1 * 500 * Width
    else:
        # Grab the price of that contract
        LongPrice = (float(SPXPutChain[iLong][BidCol]) + float(SPXPutChain[iLong][OfrCol]))/2
        # Calculate/update the rest of the output variables
        Credit = abs(round((ShortPrice - LongPrice)*100, 2))
    Risk = (500 * Width) - Credit
    Active =  True
    Index = iMinDelta

    return Credit, Risk, ShortPutStrike, Active, Index, ExpDate

def OpenCCSSPX(Delta, Width, IndexOffset, DTE, Day):
    """Calculates value for selling a CCS on SPX for a given delta on that date.

    Extended Summary
    ----------------
    Finds the credit and risk assigned for selling a CCS on SPX for a given delta using a given width
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

    DatePrevCloseS = DatePrevClose.strftime("%Y") + DatePrevClose.strftime("%m") + DatePrevClose.strftime("%d")
    ExpDate = Day + dt.timedelta(days=DTE)
    ExpDateS = ExpDate.strftime("%Y") + ExpDate.strftime("%m") + ExpDate.strftime("%d")

    DeltaDiff = 1
    DeltaDiffPrev = 1000

    for i in range(IndexOffset, len(SPXCallsChain)):
        # This will find the short put location and will exit if that option DNE
        if SPXCallsChain[i][DayCol] == DatePrevCloseS and SPXCallsChain[i][ExpCol] == ExpDateS and\
              float(SPXCallsChain[i][DelCol]) < (Delta * 1.5) and \
                  float(SPXCallsChain[i][DelCol]) > (Delta * 0.66):
            OptDelta = float(SPXCallsChain[i][DelCol])
            DeltaDiff = abs(OptDelta -  Delta)

            if DeltaDiff < DeltaDiffPrev:
                DeltaDiffPrev = DeltaDiff
                iMinDelta = i
        # Exit function early if we cannot find a short put that matches the criteria
        elif (SPXCallsChain[i][DayCol] == ExpDateS or i == (len(SPXCallsChain)-1)) and DeltaDiff > 0.1:
            Credit = 0; Risk = 0; ShortPutStrike = 0; Active = 0; Index = IndexOffset; ExpDate = 0
            return Credit, Risk, ShortPutStrike, Active, Index, ExpDate

    PIndex = SPXCallsChain[iMinDelta][SymCol][6:].find("C")
    ShortPutStrike = int(SPXCallsChain[iMinDelta][SymCol][6+PIndex+1:6+PIndex+5])
    ShortPrice = (float(SPXCallsChain[iMinDelta][BidCol]) + float(SPXCallsChain[iMinDelta][OfrCol]))/2
    # ShortPutSymbol = SPXPutChain[i][SymCol]

    LongPutSymbol = ShortPutStrike - Width*5
    LongPutSymbol = str(LongPutSymbol)
    LongPutSymbol = "SPXW " + ExpDate.strftime("%y") + ExpDate.strftime("%m")\
         + ExpDate.strftime("%d") + "C" + LongPutSymbol + "000"
    
    # Loop back over the chain and look for the long put symbol
    for i in range(IndexOffset, len(SPXCallsChain)):
        if SPXCallsChain[i][SymCol] == LongPutSymbol and SPXCallsChain[i][DayCol] == DatePrevCloseS: break

    LongPrice = (float(SPXCallsChain[i][BidCol]) + float(SPXCallsChain[i][OfrCol]))/2

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