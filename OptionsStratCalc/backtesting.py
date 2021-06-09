import numpy as np
import csv
import math
import datetime
import matplotlib.pyplot as plt
import optionsCalc as OC
import pricing_test as ivadj
from scipy import stats

def PCS_SPY(TradeNumbers, StartDate, DataFiles, IVAdjust):
    """Runs the profit/account balances of selling short term credit spreads on symbols w/ 3x weekly options.

    Extended Summary
    ----------------
    This function is used to calculate the fair market pricing for a derivative of a security
    using the Black-Scholes formula for a given strike price and time until expiration. This 
    formula works for both Calls and Puts, but does assume that that options are European style.

    Parameters
    ----------
    TradeNumbers : np.array
        [account balance, maximum risk % per trade, delta-value, credit recieved closing %]

    StartDate : datetime
        Initial starting date of the backtesting period

    DataFiles : list 
        List of data files that contain the historical data

    IVAdjust : list 
        List of linear regressions to update IV based upon like market data correlation

    Returns
    -------
    StratInfo : np.array
        Array containing the following information:
        [final account balance, number of trades, amount spent in comissions, ...
        number of day trades, number of trades fully lost, number of trades partially lost, ...
        amount spent on taxes, final account balance if bought and held SPY]
    """
    # Create linear regression functions that map VIX -> IV for different DTEs, [1-7]
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    SPYData = "spy_testing_data"
    SPYPrices = "spy_historical_data"
    VIXPrices = "vix_historical_data"
    IVFits = OC.impv_rel(Folder, SPYData, SPYPrices, VIXPrices, 8)

    # SPY IV Adjuster
    #VIXAdj = ivadj.spy_iv_adjust()

    # Output array
    StratInfo = np.zeros([8,1])

    # Read in our Data Files and look for the columns that represent Dates, Open, and Close prices
    with open(DataFiles[0]) as SPYHist:
        SPYHistorical = list(csv.reader(SPYHist))

    with open(DataFiles[1]) as VIXHist:
        VIXHistorical = list(csv.reader(VIXHist))

    with open(DataFiles[2]) as TNXHist:
        TNXHistorical = list(csv.reader(TNXHist))

    for i in range(len(SPYHistorical[0])):
        if SPYHistorical[0][i] == "Date": SPYDateCol = i; continue
        elif SPYHistorical[0][i] == "Open": SPYOpenCol = i; continue
        elif SPYHistorical[0][i] == "Close": SPYCloseCol = i; continue

    for i in range(len(VIXHistorical[0])):
        if VIXHistorical[0][i] == "Date": VIXDateCol = i; continue
        elif VIXHistorical[0][i] == "Open": VIXOpenCol = i; continue
        elif VIXHistorical[0][i] == "Close": VIXCloseCol = i; continue

    for i in range(len(TNXHistorical[0])):
        if TNXHistorical[0][i] == "Date": TNXDateCol = i; continue
        elif TNXHistorical[0][i] == "Open": TNXOpenCol = i; continue
        elif TNXHistorical[0][i] == "Close": TNXCloseCol = i; continue
    
    del SPYHist
    del VIXHist
    del TNXHist

    # Forces the trades to begin on a M-W-F cycle, might skip 1 trade ¯\_(ツ)_/¯
    Offset = 1
    if StartDate.strftime("%a") == "Tue" or "Thu" or "Sun":
        Offset +=1
    elif StartDate.strftime("%a") == "Sat":
        Offset +=2

    # Convert out lists into arrays for speed
    SPYHistorical = np.array(SPYHistorical[1:])
    VIXHistorical = np.array(VIXHistorical[1:])
    TNXHistorical = np.array(TNXHistorical[1:])

    # Buy-And-Hold Approach
    NumberShares = round(TradeNumbers[0] / float(SPYHistorical[0][SPYOpenCol]))


    position = False
    # Outer loop that runs from the start date to the final date
    for iDate in range(Offset-1, len(TNXHistorical)-1):
        # Sets the maximum amount that can be risked in any given trade
        MaxRisk = TradeNumbers[0] * TradeNumbers[1]

        # Grab the open/close prices from historical data & linear interpolate
        SPYOpen = float(SPYHistorical[iDate][SPYOpenCol])
        SPYClose = float(SPYHistorical[iDate][SPYCloseCol])

        VIXOpen = float(VIXHistorical[iDate][VIXOpenCol])
        VIXClose = float(VIXHistorical[iDate][VIXCloseCol])

        TNXOpen = float(TNXHistorical[iDate][TNXOpenCol])
        TNXClose = float(TNXHistorical[iDate][TNXCloseCol])

        # One data point per half hour, 6.5 hours + open/lose -> 15 points
        SPYIntraday = np.linspace(SPYOpen, SPYClose, 15) 
        VIXIntraday = np.linspace(VIXOpen, VIXClose, 15)
        TNXIntraday = np.linspace(TNXOpen, TNXClose, 15)

        # Get the current day to check for DTE
        CurrentDay = (datetime.datetime(int(SPYHistorical[iDate][SPYDateCol][0:4]), 
            int(SPYHistorical[iDate][SPYDateCol][4:6]), int(SPYHistorical[iDate][SPYDateCol][6:8])))

        # Width
        Width = 2
        # Check to see if there is a position open, if not open the trade
        if position == False:
            # Finds DTE if we're for the MWF trading schedule
            if CurrentDay.strftime("%a") == "Mon" or "Wed":
                DTE = 2
            elif CurrentDay.strftime("%a") == "Fri":
                DTE = 3
            else:
                continue

            # Start at-the-money and begin to go down in strike to find a short option
            for iShort in range(100):
                # Grab the necessary information for calculating price on BS
                Strike = math.floor(SPYOpen)-iShort
                IV = IVFits[DTE-1].slope * VIXOpen + IVFits[DTE-1].intercept

                # Short option strike > Long option strike by 1
                ShortPut = OC.black_scholes("SPY", SPYOpen, Strike, TNXOpen/100, DTE, IV/100, "P")
                # MoneynessShort = Strike - SPYOpen
                LongPut = OC.black_scholes("SPY", SPYOpen, Strike-Width, TNXOpen/100, DTE, IV/100, "P")
                # MoneynessLong = (Strike-Width) - SPYOpen

                # If we are less than our Delta amount, exit the loop as the spread meets requirements
                if abs(ShortPut.delta) <= TradeNumbers[2]:
                    break
            
            # # Update the prices of the short and long positions based on their moneyness
            # ShortPutPrice = ShortPut.price + (VIXAdj[DTE-1].slope * MoneynessShort + VIXAdj[DTE-1].intercept)
            # LongPutPrice = LongPut.price + (VIXAdj[DTE-1].slope * MoneynessLong + VIXAdj[DTE-1].intercept)
            
            # Net Credit of the spread
            NetCredit = abs(round(ShortPut.price - LongPut.price, 2))

            # Defined risk = Width - Credit
            SpreadRisk = (Width-NetCredit) * 100

            # Maximum number of spreads to fit within our risk profile
            NumberSpreads = math.floor(MaxRisk / SpreadRisk)

            # Date the spread must be closed by
            DateForceClose = CurrentDay + datetime.timedelta(days=DTE)

            # Assume a position is open and update it 
            position = True

        # Now that a position is open we need to go through intraday and check
        # to see if that position needs to be closed, and update balances accordingly
        if position == True:
            # Iterate over the linspace'd open/close prices and check to see if the position is closed
            for iIntraday in range(len(SPYIntraday)):
                SPYPrice = SPYIntraday[iIntraday]
                RFRR = TNXIntraday[iIntraday]

                if DTE == 0:
                    IV = IVFits[0].slope * VIXIntraday[iIntraday] + IVFits[0].intercept
                    TTE = 1 - iIntraday/14
                elif DTE != 0:
                    TTE = DTE - (iIntraday/14) 
                    IV = IVFits[DTE-1].slope * VIXIntraday[iIntraday] + IVFits[DTE-1].intercept
                
                # Calculate the new current value of the spread and check to see if we can close it
                ShortPutIntraday = OC.black_scholes("SPY", SPYPrice, Strike, RFRR/100, TTE, IV/100, "P")
                LongPutIntraday = OC.black_scholes("SPY", SPYPrice, Strike-Width, RFRR/100, TTE, IV/100, "P")
                
                # MoneynessShortIntraday = Strike - SPYPrice
                # MoneynessLongIntraday = (Strike-Width) - SPYPrice

                # if DTE == 0: 
                #     ShortPutIntradayPrice = ShortPutIntraday.price + (VIXAdj[0].slope * MoneynessShortIntraday + VIXAdj[0].intercept)
                #     LongPutIntradayPrice = LongPutIntraday.price + (VIXAdj[0].slope * MoneynessLongIntraday + VIXAdj[0].intercept)
                # elif DTE != 0:
                #     ShortPutIntradayPrice = ShortPutIntraday.price + (VIXAdj[DTE-1].slope * MoneynessShortIntraday + VIXAdj[DTE-1].intercept)
                #     LongPutIntradayPrice = LongPutIntraday.price + (VIXAdj[DTE-1].slope * MoneynessLongIntraday + VIXAdj[DTE-1].intercept)

                ClosingDebit =  abs(round(ShortPutIntraday.price - LongPutIntraday.price, 2))

                # Checkt to see if the position has made enough credit via theta-decay to 
                # close the position and update balances and such
                if ClosingDebit <= (TradeNumbers[3] * NetCredit) or ((CurrentDay == DateForceClose) and iIntraday == len(SPYIntraday)):

                    # Close the position
                    position = False

                    # If we're at DTE = 0 & hit the end of intra day and still haven't closed, then it is
                    # a partial/maximum loss trade
                    if DTE == 0 and iIntraday == len(SPYIntraday):
                        
                        # Check for maximum loss trade
                        if SPYIntraday[iIntraday] <= (Strike-1):
                            # Add one to the maximum loss counter
                            StratInfo[4] += 1 
                            # Account for comissions w/ opening/closing
                            Comissions = 2
                            # Subtract the total risked amount from the account balance
                            TradeNumbers[0] = TradeNumbers[0] - (SpreadRisk * NumberSpreads - Comissions)
                            StratInfo[2] += Comissions

                        # Check for partially lost trades
                        elif SPYIntraday[iIntraday] < (Strike) and SPYIntraday[iIntraday] >= (Strike-1):
                            # Add one to the partial loss counter
                            StratInfo[3] +=1
                            # Account for comissions w/ opening/closing
                            Comissions = 2
                            # Check to see if any revenue was made
                            Revenue = NumberSpreads * (NetCredit - ClosingDebit)
                            if Revenue <= 0: Taxes = 0 
                            elif Revenue > 0: Taxes = Revenue * 0.33
                            # Add the revnue to the account balance
                            TradeNumbers[0] = TradeNumbers[0] + (Revenue - Taxes - Comissions)
                            StratInfo[2] += Comissions
                            StratInfo[6] += Taxes
                        
                    # If neither of those losses are met, then we've made maximum profit
                    elif SPYIntraday[iIntraday] >= Strike:
                        # Update various balances and check for things like losses and/or day trades
                        Revenue =  NumberSpreads * (NetCredit - ClosingDebit) * 100
                        Taxes = Revenue * 0.33
                        Comissions = 2
                        TradeNumbers[0] = TradeNumbers[0] + (Revenue -  Taxes - Comissions)
                        StratInfo[2] += Comissions
                        StratInfo[6] += Taxes
                        break

        # Every time we iterate, go down in DTE
        if DTE > 0:
            DTE -= 1
    
    StratInfo[0] = TradeNumbers[0]
    StratInfo[7] = NumberShares * SPYClose
    return StratInfo