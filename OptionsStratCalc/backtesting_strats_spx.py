from ast import Num
import numpy as np
import os
import csv
import math
import datetime as dt
import random

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
        average return on collateral, number of simulated trades using average returns]
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
    BacktestResults = np.zeros([11,1])
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
    Simulation = False
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

            # If we had to simulate the position, simulate the closing using the delta value (~ PoP)
            if Simulation:
                BacktestResults[10] += 1
                Chance = random.random()
                # If we're less than the delta, it will be a complete loss
                if Chance <= TradeParameters[2]:
                    Strike = SPXC * 2
                # If nore, then it is a complete win
                else:
                    Strike = SPXC - 1

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
            if Profit > 0: Taxes = Profit * 0.25
            else: Taxes = 0
            
            # Add to our account balances
            TradeParameters[0] += Profit - Taxes
            BacktestResults[0] += Profit - Taxes
            BacktestResults[7] += Taxes

            # Add the % credit for collateral
            if Simulation: PercentReturn = random.randrange(1, 10) / 100
            else: PercentReturn = (Credit - Fees) / (500 * Width - Credit)
            ReturnOnCollateral = np.append(ReturnOnCollateral, PercentReturn)

            # Update our position
            Position = False
            Simulation = False

        if (Weekday == "Mon" or Weekday == "Wed") and not Position:
            DTE = 2
            Credit, Risk, Strike, Position, PrevIndex, ExpDate, Simulation = \
                OpenPCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay, ReturnOnCollateral)

        elif (Weekday == "Fri") and not Position:
            DTE = 3
            Credit, Risk, Strike, Position, PrevIndex, ExpDate, Simulation = \
                OpenPCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay, ReturnOnCollateral)
        
    BacktestResults[9] = np.mean(ReturnOnCollateral) * 100
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
        average return on collateral, number of simulated trades using average returns]
    """
    global SPXHistPrice, SPXCallChain
    global SymCol, BidCol, OfrCol, DelCol, DayCol, ExpCol
    # Load in all our data for testing
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"

    SPXHistPrice = "SPX_daily_prices.csv"
    SPXCallChain = "Calls2.csv"
    # SPXCallChain = "SPXCallsChain.csv"

    SPXHistPrice = os.path.join(Folder, SPXHistPrice)
    SPXCallChain = os.path.join(Folder, SPXCallChain)

    # Output array
    BacktestResults = np.zeros([11,1])
    ReturnOnCollateral = np.empty([0])

    # Read in the data files
    with open(SPXHistPrice) as DataFile:
        SPXHistPrice = list(csv.reader(DataFile))

    with open(SPXCallChain) as DataFile:
        SPXCallChain = list(csv.reader(DataFile))
    # SPXCallChain.reverse()

    # Grab the needed columns from each data file
    Header = np.array(SPXHistPrice[0])
    # OpnCol = int(np.where(Header == "Open")[0])
    ClsCol = int(np.where(Header == "close")[0])
    HDTCol = int(np.where(Header == "date")[0])

    Header = np.array(SPXCallChain[0])
    DayCol = int(np.where(Header == "date")[0])
    SymCol = int(np.where(Header == "symbol")[0])
    BidCol = int(np.where(Header == "best_bid")[0])
    OfrCol = int(np.where(Header == "best_offer")[0])
    DelCol = int(np.where(Header == "delta")[0])
    ExpCol = int(np.where(Header == "exdate")[0])

    # Convert for speed
    SPXHistPrice = np.array(SPXHistPrice[1:])
    SPXCallChain = np.array(SPXCallChain[1:])

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
    Simulation = False
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
            
            # If we had to simulate the position, simulate the closing using the delta value (~ PoP)
            # This checks for the put leg
            if Simulation:
                BacktestResults[10] += 1
                Chance = random.random()
                # If we're less than the delta, it will be a complete loss
                if Chance <= TradeParameters[2]:
                    Strike = SPXC / 2
                # If nore, then it is a complete win
                else:
                    Strike = SPXC + 1


            # Break even price 
            Breakeven =  Strike + Credit/100
            
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
            if Profit > 0: Taxes = Profit * 0.25
            else: Taxes = 0
            
            # Add to our account balances
            TradeParameters[0] += Profit - Taxes
            BacktestResults[0] += Profit - Taxes
            BacktestResults[7] += Taxes

            # Add the % credit for collateral - randomize it if simulated as we don't know actual return
            if Simulation: PercentReturn = random.randrange(1, 10) / 100
            else: PercentReturn = (Credit - Fees) / (500 * Width - Credit)
            ReturnOnCollateral = np.append(ReturnOnCollateral, PercentReturn)

            # Update our position
            Position = False
            Simulation = False

        if (Weekday == "Mon" or Weekday == "Wed") and not Position:
            DTE = 2
            Credit, Risk, Strike, Position, PrevIndex, ExpDate, Simulation = \
                OpenCCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay, ReturnOnCollateral)

        elif (Weekday == "Fri") and not Position:
            DTE = 3
            Credit, Risk, Strike, Position, PrevIndex, ExpDate, Simulation = \
                OpenCCSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay, ReturnOnCollateral)
               
        
    BacktestResults[9] = np.mean(ReturnOnCollateral) * 100
    return BacktestResults

def ICS_SPX(TradeParameters, StartDate, ScalingMethod):
    """Backtests selling M2W, W2F, and F2M Iron Condors on SPX and resulting gains/losses.

    Extended Summary
    ----------------
    Backtests selling Iron Condors at market open and letting them run and either buying to close, or letting
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
        average return on collateral, number of simulated trades using average returns]
    """
    global SPXHistPrice, SPXCallChain, SPXPutChain
    global SymCol, BidCol, OfrCol, DelCol, DayCol, ExpCol

    # Load in all our data for testing
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"

    SPXHistPrice = "SPX_daily_prices.csv"
    SPXCallChain = "Calls2.csv"
    SPXPutChain = "Puts.csv"
    # SPXCallChain = "SPXCallsChain.csv"

    SPXHistPrice = os.path.join(Folder, SPXHistPrice)
    SPXCallChain = os.path.join(Folder, SPXCallChain)
    SPXPutChain = os.path.join(Folder, SPXPutChain)

    # Output array
    BacktestResults = np.zeros([11,1])
    ReturnOnCollateral = np.empty([0])

    # Read in the data files
    with open(SPXHistPrice) as DataFile:
        SPXHistPrice = list(csv.reader(DataFile))

    with open(SPXPutChain) as DataFile:
        SPXPutChain = list(csv.reader(DataFile))

    with open(SPXCallChain) as DataFile:
        SPXCallChain = list(csv.reader(DataFile))

    # Grab the needed columns from each data file
    Header = np.array(SPXHistPrice[0])
    # OpnCol = int(np.where(Header == "Open")[0])
    ClsCol = int(np.where(Header == "close")[0])
    HDTCol = int(np.where(Header == "date")[0])

    Header = np.array(SPXCallChain[0])
    DayCol = int(np.where(Header == "date")[0])
    SymCol = int(np.where(Header == "symbol")[0])
    BidCol = int(np.where(Header == "best_bid")[0])
    OfrCol = int(np.where(Header == "best_offer")[0])
    DelCol = int(np.where(Header == "delta")[0])
    ExpCol = int(np.where(Header == "exdate")[0])

    # Convert for speed
    SPXHistPrice = np.array(SPXHistPrice[1:])
    SPXCallChain = np.array(SPXCallChain[1:])
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
    Fees = 5.08

    # Initialize our position and misc parameters
    Position = False
    Simulations = [False, False]
    PrevIndex = [0,0]
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

            # If we had to simulate the position, simulate the closing using the delta value (~ PoP)
            if Simulations[0] or Simulations[1]:
                BacktestResults[10] += 1
                Chance = random.random()
                if Simulations[0]:
                    # If we're less than the delta, PCS side is broken, partial loss on PCS
                    if Chance <= TradeParameters[2]:
                        Strikes[0] = SPXC * 2
                if Simulations[1]:
                    # If we're above 1-delta, then CCS is broken, partial loss on CCS 
                    if Chance >= (1 - TradeParameters[2]):
                        Strikes[1] = SPXC / 2
                if Simulations[0] and Simulations[1]:
                    # If we're 100% ITM then we have to have strikes that fit accordingly
                    if Chance > TradeParameters[2] and Chance < (1 - TradeParameters[2]):
                        Strikes[0] = SPXC - 1
                        Strikes[1] = SPXC + 1
                    # If we're above 1-delta, then CCS is broken, partial loss on CCS 
                    elif Chance >= (1 - TradeParameters[2]):
                        Strikes[1] = SPXC / 2
                        Strikes[0] = SPXC - 1
                    # If we're less than the delta, PCS side is broken, partial loss on PCS
                    elif Chance <= TradeParameters[2]:
                        Strikes[0] = SPXC * 2
                        Strikes[1] = SPXC + 1

            # Break even price 
            BreakevenP = Strikes[0] - (Credits[0] + Credits[1])/100
            BreakevenC = Strikes[1] + (Credits[0] + Credits[1])/100
            
            # Calculate number of spreads and fees to be paid
            NumberSpreads = (MaxRisk / Risk)
            if NumberSpreads < 1: NumberSpreads = 1
            else: NumberSpreads = math.floor(NumberSpreads)

            TotalFees = NumberSpreads * Fees

            BacktestResults[1] += 1 # add to times traded
            BacktestResults[2] += NumberSpreads # add to number of spreads traded
            BacktestResults[8] += TotalFees # add to amount paid in comissions

            # Condition 1 - full win with SPXC between the two strikes
            if SPXC > Strikes[0] and SPXC < Strikes[1]:
                Profit = (Credits[0] + Credits[1]) * NumberSpreads - TotalFees
                BacktestResults[3] += 1

            # Condition 2A - Partial win on put side
            elif SPXC > BreakevenP:
                Profit = ((Credits[0] - (Strikes[0] - SPXC)) * NumberSpreads) - TotalFees + (Credits[1] * NumberSpreads)
                BacktestResults[4] +=1

            # Condition 2B - Partial win on call side
            elif SPXC < BreakevenC:
                Profit = ((Credits[1] - (Strikes[1] - SPXC)) * NumberSpreads) - TotalFees + (Credits[0] * NumberSpreads)
                BacktestResults[4] +=1

            # Condition 3A - Put leg is broken and need to BTC the put position
            elif SPXC < (Strikes[0]-5*Width):
                Profit = ((Credits[0] - (Strikes[0] - SPXC)) * NumberSpreads) - TotalFees - (2.5 * Credits[1])
                BacktestResults[5] +=1

            # Condition 3B - Call leg is broken and need to BTC the call position
            elif SPXC > (Strikes[1]+5*Width):
                Profit = ((Credits[1] - (Strikes[1] - SPXC)) * NumberSpreads) - TotalFees - (2.5 * Credits[0])
                BacktestResults[5] +=1

            # Calculate the amount of taxes to be paid
            if Profit > 0: Taxes = Profit * 0.25
            else: Taxes = 0
            
            # Add to our account balances
            TradeParameters[0] += Profit - Taxes
            BacktestResults[0] += Profit - Taxes
            BacktestResults[7] += Taxes

            # Add the % return on collateral
            if Simulations[0] or Simulations[1]: PercentReturn = random.randrange(5, 15) / 100
            elif not Simulations[0] and not Simulations[1]: 
                PercentReturn = (Credits[0] + Credits[1]) / (500 * Width - (Credits[0] + Credits[1]))
            ReturnOnCollateral = np.append(ReturnOnCollateral, PercentReturn)

            # Update our position
            Position = False
            Simulations[0] = False
            Simulations[1] = False

        if (Weekday == "Mon" or Weekday == "Wed") and not Position:
            DTE = 2
            Credits, Risk, Strikes, Position, PrevIndex, ExpDate, Simulations = \
                OpenICSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay, ReturnOnCollateral)

        elif (Weekday == "Fri") and not Position:
            DTE = 3
            Credits, Risk, Strikes, Position, PrevIndex, ExpDate, Simulations = \
                OpenICSSPX(TradeParameters[2], Width, PrevIndex, DTE, CurrentDay, ReturnOnCollateral)



    BacktestResults[9] = np.mean(ReturnOnCollateral) * 100
    return BacktestResults

def OpenPCSSPX(Delta, Width, IndexOffset, DTE, Day, RoC):
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
    
    RoC : np.array
        Array of the average premium per collateral, used when we have to simulate the trade


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

    Simulation : boolean
        Updates if the trade was simulated or not
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
    # need to simulate the trade cycle
    if MinDelta > 0.5:
        # Simulate the trade using the average returns 
        AverageRoC = np.mean(RoC)
        Collateral = 500 * Width
        # Total amount of return and risk involved
        Credit = AverageRoC * Collateral 
        Risk = Collateral - Credit

        Index = IndexOffset
        # Update the position
        Active = True
        Simulation =  True
        # Strike doesn't matter, simulating the trade based on probability
        ShortPutStrike = 0

        return Credit, Risk, ShortPutStrike, Active, Index, ExpDate, Simulation

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
    Simulation = False
    Index = iMinDelta

    return Credit, Risk, ShortPutStrike, Active, Index, ExpDate, Simulation

def OpenCCSSPX(Delta, Width, IndexOffset, DTE, Day, RoC):
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

    RoC : np.array
        Array of the average premium per collateral, used when we have to simulate the trade


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

    Simulation : boolean
        Updates if the trade was simulated or not
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

    DeltaDiff = 1
    MinDelta = 1000

    for i in range(IndexOffset, len(SPXCallChain)):
        # This will find the short put that is closest to the delta that we want,
        # and will exit the loop if that option DNE
        if SPXCallChain[i][DayCol] == DatePrevCloseS and SPXCallChain[i][ExpCol] == ExpDateS and\
            float(SPXCallChain[i][DelCol]) < (Delta * 1.1):
            # Grab the delta of this contract in the loop, find the difference to our set delta
            OptDelta = float(SPXCallChain[i][DelCol])
            DeltaDiff = abs(OptDelta -  Delta)
            # If a new smaller delta difference is found, update it and record that row
            if DeltaDiff < MinDelta:
                MinDelta = DeltaDiff
                iMinDelta = i
        # Exit function early if we cannot find a short put that matches the criteria
        elif (SPXCallChain[i][DayCol] == ExpDateS or i == (len(SPXCallChain)-1)): break
    # If we have too big of a variance, it means we cannot find a spread to fit our criteria and
    # just need to skip this trade cycle
    if MinDelta > 0.5:
        # Simulate the trade using the average returns 
        AverageRoC = np.mean(RoC)
        Collateral = 500 * Width
        # Total amount of return and risk involved
        Credit = AverageRoC * Collateral 
        Risk = Collateral - Credit

        Index = IndexOffset
        # Update the position
        Active = True
        Simulation =  True
        ShortCallStrike = 0

        return Credit, Risk, ShortCallStrike, Active, Index, ExpDate, Simulation
        
    # Need to know string information for the symbol column to find the strike
    PIndex = SPXCallChain[iMinDelta][SymCol][6:].find("C")
    ShortCallStrike = int(SPXCallChain[iMinDelta][SymCol][6+PIndex+1:6+PIndex+5])
    # Grab the price of our short position   
    ShortPrice = (float(SPXCallChain[iMinDelta][BidCol]) + float(SPXCallChain[iMinDelta][OfrCol]))/2
    # ShortPutSymbol = SPXPutChain[i][SymCol]

    # Rebuild the symbol for our long position
    LongCallSymbol = ShortCallStrike + Width*5
    LongCallSymbol = str(LongCallSymbol)
    LongCallSymbol = "SPXW " + ExpDate.strftime("%y") + ExpDate.strftime("%m")\
         + ExpDate.strftime("%d") + "C" + LongCallSymbol + "000"
    
    # Loop back over the chain and look for the long put symbol
    for iLong in range(IndexOffset, len(SPXCallChain)):
        if SPXCallChain[iLong][SymCol] == LongCallSymbol and SPXCallChain[iLong][DayCol] == DatePrevCloseS: break
    # If we can't find the appropriate long put contract, assume credit is ~10% of the width
    # if iLong == 4572522: Credit = 0.1 * 500 * Width
    if iLong == 824015: Credit = 0.1 * 500 * Width
    else:
        # Grab the price of that contract
        LongPrice = (float(SPXCallChain[iLong][BidCol]) + float(SPXCallChain[iLong][OfrCol]))/2
        # Calculate/update the rest of the output variables
        Credit = abs(round((ShortPrice - LongPrice)*100, 2))
    Risk = (500 * Width) - Credit
    Active =  True
    Simulation = False
    Index = i

    return Credit, Risk, ShortCallStrike, Active, Index, ExpDate, Simulation

def OpenICSSPX(Delta, Width, IndexOffset, DTE, Day, RoC):
    """Calculates value for selling a Iron Condor on SPX for a given delta on that date.

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

    RoC : np.array
        Array of the average premium per collateral, used when we have to simulate the trade


    Returns
    -------
    Credit : float tuple
        Credit received for the PCS and CCS

    Risk : float
        Amount of money used as collateral for the IC

    Strike : int tuple
        Tuple of the PCS and CCS strikes

    Active : boolean
        Updates the position to be true

    Index : int
        New index for looping when checking value of the spread

    Simulation : boolean
        Updates if the trade was simulated or not
    """
    # Use the PCS function to open the put leg
    CreditP, _, StrikeP, ActiveP, IndexP, ExpDateP, SimulationP = \
        OpenPCSSPX(Delta, Width, IndexOffset[0], DTE, Day, RoC)

    # Use the CCS function to open the call leg
    CreditC, _, StrikeC, ActiveC, IndexC, ExpDateC, SimulationC = \
        OpenCCSSPX(Delta, Width, IndexOffset[1], DTE, Day, RoC)

    # Total credit for the trade is
    CreditT = CreditC + CreditP

    # Maximum total risk for the trade
    RiskT = (500 * Width) - CreditT

    # Sanity check to make sure both positions are active and same expiration
    if ActiveP and ActiveC: Active = True
    if ExpDateC == ExpDateP: ExpDate = ExpDateP

    return [CreditP, CreditC], RiskT, [StrikeP, StrikeC], Active, [IndexP, IndexC], ExpDate, [SimulationP, SimulationC]


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