import numpy as np
import csv
import math
import datetime
import optionsCalc as OC
import historical_price_adj as hpa


def PCS_SPY(TradeParameters, StartDate, DataFiles):
    """Runs the profit/account balances of selling short term credit spreads on symbols w/ 3x weekly options.

    Extended Summary
    ----------------
    This function is used to calculate the fair market pricing for a derivative of a security
    using the Black-Scholes formula for a given strike price and time until expiration. This 
    formula works for both Calls and Puts, but does assume that that options are European style.

    Parameters
    ----------
    TradeParameters : np.array
        [account balance, maximum risk % per trade, delta-value, credit recieved closing %]

    StartDate : datetime
        Initial starting date of the backtesting period

    DataFiles : list 
        List of data files that contain the historical data

    IVAdjust : list 
        List of linear regressions to update IV based upon live market data correlation

    Returns
    -------
    BacktestResults : np.array
        Array containing the following information:
        [final account balance, number of trades, amount spent in comissions, ...
        number of day trades, number of trades fully lost, number of trades partially lost, ...
        amount spent on taxes, final account balance if bought and held SPY, number of spreads traded, ...
        number of times a stop loss saved us from maximum loss]
    """
    # Create linear regression functions that map VIX -> IV for different DTEs, [1-7]
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    SPYData = "spy_testing_data"
    SPYPrices = "spy_historical_data"
    VIXPrices = "vix_historical_data"
    IVFits = OC.impv_rel(Folder, SPYData, SPYPrices, VIXPrices, 8)

    # # Create our price adjuster for the historical pricings
    # PricingCoeffs = hpa.historicalPriceAdj()
    PricingCoeffs = 0

    # Output array
    BacktestResults = np.zeros([10,1])

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
        # if VIXHistorical[0][i] == "Date": VIXDateCol = i; continue
        if VIXHistorical[0][i] == "Open": VIXOpenCol = i; continue
        elif VIXHistorical[0][i] == "Close": VIXCloseCol = i; continue

    for i in range(len(TNXHistorical[0])):
        # if TNXHistorical[0][i] == "Date": TNXDateCol = i; continue
        if TNXHistorical[0][i] == "Open": TNXOpenCol = i; continue
        elif TNXHistorical[0][i] == "Close": TNXCloseCol = i; continue
    
    del SPYHist
    del VIXHist
    del TNXHist

    Offset = 0
    # Forces the trades to begin on the start date, and then adjust to the M-W-F cycle
    DateIndex = str(StartDate.strftime("%Y"))\
         + str(StartDate.strftime("%m")) + str(StartDate.strftime("%d"))
    for iDate in range(len(SPYHistorical)):
        if SPYHistorical[iDate][SPYDateCol] == DateIndex: Offset = iDate; break
    
    if StartDate.strftime("%a") == "Tue" or "Thu" or "Sun":
        Offset +=1
    elif StartDate.strftime("%a") == "Sat":
        Offset +=2

    # Convert out lists into arrays for speed
    SPYHistorical = np.array(SPYHistorical[1:])
    VIXHistorical = np.array(VIXHistorical[1:])
    TNXHistorical = np.array(TNXHistorical[1:])

    # Initialize our current open position
    Position = False

    # Comissions and fees per spread from using Tastyworks
    Comissions = 2
    Fees = 0.27

    # Outer loop that runs from the start date to the final date
    for iDate in range(Offset, len(TNXHistorical)-1):

        # Sets the maximum amount that can be risked in any given trade
        MaxRisk = TradeParameters[0] * TradeParameters[1]
        if MaxRisk > 10000:
            MaxRisk = 10000

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
            int(SPYHistorical[iDate][SPYDateCol][4:6]),
            int(SPYHistorical[iDate][SPYDateCol][6:8])))

        # Width of spread
        Width = 1
        
        # Finds DTE if we're for the MWF trading schedule and the position is currently closed
        # Only resets to MWF position if we have no open positions and it is one of those 3 days
        if (CurrentDay.strftime("%a") == "Mon" or "Wed") and (Position == False):
            DTE = 2
        elif (CurrentDay.strftime("%a") == "Fri") and (Position == False):
            DTE = 3

        # Inner loop that goes throughout the days
        for iIntraday in range(len(SPYIntraday)):

            # If the position is currently close (false), open a position
            if Position == False:
                Credit, Risk, Position, Strike = OpenPCSSPY(CurrentDay.year, DTE, SPYIntraday[iIntraday],\
                     VIXIntraday[iIntraday], TNXIntraday[iIntraday], TradeParameters[2], Width,\
                         IVFits, PricingCoeffs, iIntraday)

                # Check the date that the spread was opened and find force close by date
                DateOpened = CurrentDay
                DateForceClose = CurrentDay + datetime.timedelta(days=DTE)

                # Maximum number of spreads is limited by the risk of each spread
                if Risk == 0: continue # Safety measure to skip trades we don't want, i.e. to small premium
                NumberSpreads = math.floor(MaxRisk / Risk)
                BacktestResults[8] += NumberSpreads

                # Total amount of comission and fees to be paid
                TotalFees = NumberSpreads * (Comissions + Fees)
                BacktestResults[2] += TotalFees

                # Add one to counter of trades done
                BacktestResults[1] += 1

            # Else if it is already open, check to see if it can be closed by checking out closing criteria
            else:
                # Three unique sets of closing criteria:
                # 1 - The spread has reached our desired cutoff point of profit to be made
                # 2 - Stop loss comes into play and it forces the position closed early
                # 3 - It is date forced closed and we've made partial profit/loss (final SPY price is between strikes of short & long)
                # 4 - It is date forced close and we've hit maximum loss (SPY is below strike of the long)

                # Day trade limiter - skips closing if we're on the same day that the position was opened
                if CurrentDay == DateOpened and TradeParameters[0] < 25001:
                    continue

                Debit = ClosePCSSPY(CurrentDay.year, DTE, SPYIntraday[iIntraday],\
                    VIXIntraday[iIntraday], TNXIntraday[iIntraday],Width,\
                        IVFits, PricingCoeffs, iIntraday, Strike)
                
                # The predefined amount of credit recieved we want to close at
                ClosingDebit = Credit * TradeParameters[3]

                # Condition 1 - we've hit enough profit to close the spread
                if Debit < ClosingDebit:
                    # Total amount of profit
                    Profit = ((Credit - Debit) * NumberSpreads) * 100

                    # Total amount paid in taxes
                    Taxes = Profit * 0.33

                    # Update the amount paid in taxes and the account balance
                    TradeParameters[0] += (Profit - Taxes - TotalFees)
                    BacktestResults[0] += (Profit - Taxes - TotalFees)
                    if CurrentDay == DateOpened: BacktestResults[3] += 1
                    BacktestResults[6] += Taxes

                    # Close the position and prepare to open a new one
                    Position = False

                # Condition 2 - stop loss kicks in
                elif Debit > (2.5*Credit):

                    # Buy to close our position and reduce balances
                    TradeParameters[0] -= (Debit * NumberSpreads + TotalFees)
                    BacktestResults[0] -= Debit * NumberSpreads
                    BacktestResults[9] += 1 # Add one to stop loss counter 

                    # Close the position and prepare to open a new one
                    Position = False

                # Conditions 3 & 4 - we're out of time and need to check for partial/total losses
                elif (DTE == 0 and iIntraday == 14) or (CurrentDay == DateForceClose and iIntraday == 14):
                    
                    # If SPY < long position, then we're at a maximum loss
                    if SPYIntraday[iIntraday] < (Strike-Width):
                        # Subtract the risked amount and fees from our currently balance, no taxes though
                        TradeParameters[0] -= (NumberSpreads * Risk + TotalFees)
                        BacktestResults[0] -= (NumberSpreads * Risk)
                        BacktestResults[4] += 1 # Add to total losses counter
                        
                        # Close the position and prepare to open a new one
                        Position = False
                        S1 = "On " + str(CurrentDay.year) + "-" + str(CurrentDay.month) + "-" + str(CurrentDay.day)
                        S2 = " we had a total loss because SPY traded at: $" + str(SPYIntraday[iIntraday])
                        S3 = " and our long-put was at a strike of $" + str(int(Strike-Width))
                        S4 = " and we lost $" + str(int(NumberSpreads * Risk))
                        print(S1 +  S2 + S3 + S4)

                    # If Long < SPY < Short, then we're at a partial loss
                    elif SPYIntraday[iIntraday] < Strike and SPYIntraday[iIntraday] > (Strike-Width):
                        Debit = ClosePCSSPY(CurrentDay.year, DTE, SPYIntraday[iIntraday],\
                            VIXIntraday[iIntraday], TNXIntraday[iIntraday],Width,\
                                IVFits, PricingCoeffs, iIntraday, Strike)

                        # Total profit, if there is any
                        Profit = ((Credit - Debit) * NumberSpreads) * 100

                        # Calculate taxes, if there is any
                        if Profit < 0: Taxes = 0
                        else: Taxes = Profit * 0.33

                        # Update the amount paid in taxes and the account balance
                        TradeParameters[0] += (Profit - Taxes - TotalFees)
                        BacktestResults[0] += (Profit - Taxes - TotalFees)
                        BacktestResults[5] += 1 # Add to partial trades counter
                        BacktestResults[6] += Taxes
                                        
                        # Close the position and prepare to open a new one
                        Position = False

        # Continue on to the next day
        if DTE > 0:
            DTE -= 1
            

    # Used to back-calculate SPY w/ dividends and such, either one works but the latter does customs numbers
    # https://www.dividendchannel.com/drip-returns-calculator/
    # https://www.portfoliovisualizer.com/backtest-portfolio#analysisResults
    BacktestResults[7] = 12530
    
    return BacktestResults

def CCS_SPY(TradeParameters, StartDate, DataFiles):

def ICS_SPY(TradeParameters, StartDate, DataFiles):

def OpenPCSSPY(Year, DTE, Mark, VIX, IR, Delta, Width, IVF, PA, Intraday):
    """Opens a put credit spread (PCS) on SPY.

    Extended Summary
    ----------------
    This function is used to calculate the credit and risk associate with opening a put credit spread on SPY
    for the given function parameters.

    Parameters
    ----------
    Year : int
        The current year in 4 digit number format.

    DTE : int
        How many full days until expiration for the spread.

    Mark : float
        Current trading price of SPY

    VIX : float
        Current trading price of VIX

    IR : float
        Current trading price/interest rate of the US 10-year treasury bond (^TNX), used to calculate the RFRR

    Delta : float
        The guage of closeness to money for the short and long options

    Width : int
        How many points the strikes are to be spaced out by

    IVF : list
        A list that contains the relationships to map VIX prices to IV for SPY

    PA : list
        A list that contains the coefficients to adjust the mathematical Black-Scholes prices to actual market prices

    Intraday : int
        How far along in the day we are - used to calculate total time until expiration (TTE)

    Returns
    -------
    Credit : int
        The total amount of credit gained before comissions, fees, and taxes

    Risk : int
        The total amount risked per spread

    Position : boolean
        Updates the Position boolean to be true
    """
    # Total time til expiration that includes intraday
    TTE = DTE + (1 - Intraday/14)

    # IV % of the option based upon VIX pricing on that day and time
    if DTE == 0:
        IV = IVF[0].slope * VIX + IVF[0].intercept
    else:
        IV = IVF[DTE-1].slope * VIX + IVF[DTE-1].intercept

    # Find the closest strike that satisfies our delta requirement
    for iStrike in range(100):
        Strike = math.floor(Mark) - iStrike
        ShortPut = OC.black_scholes("N/A", Mark, Strike, IR/100, TTE, IV/100, "P")

        # If the delta requirement is met, break the loop
        if abs(ShortPut.delta) <= Delta:
            break

    # Now find the long position - our insurance position
    LongPut = OC.black_scholes("N/A", Mark, Strike - Width, IR/100, TTE, IV/100, "P")

    # # Need moneyness of both options to adjust prices post calculation - this is information
    # # was found by looking at 10 years worth of market data for SPY
    # MoneynessShort = Strike -  Mark
    # MoneynessLong = (Strike -  Width) - Mark

    # # Grab the differences in price from our given SPY data samply
    # PriceDiffShort = PA[Year-2010][DTE-1][0]\
    #      * np.exp(-PA[Year-2010][DTE-1][1] * MoneynessShort**2 * 0.5) / (2*np.pi)
    # PriceDiffLong = PA[Year-2010][DTE-1][0]\
    #      * np.exp(-PA[Year-2010][DTE-1][1] * MoneynessLong**2 * 0.5) / (2*np.pi)

    # # Apply our differential
    # PriceShort = ShortPut.price - PriceDiffShort
    # PriceLong = LongPut.price - PriceDiffLong

    # Net Credit for opening the spread
    Credit = (round(ShortPut.price - LongPut.price, 2))

    # Check to see if it is worth opening - comissions & fees don't take away all the profit
    if (100 * Credit) < 10:
        Position = False
        Risk = 0
        return Credit, Risk, Position, Strike

    # Risk of the spread
    Risk = (Width - Credit) * 100

    # Update the position so that it is true
    Position =  True

    return Credit, Risk, Position, Strike

def ClosePCSSPY(Year, DTE, Mark, VIX, IR, Width, IVF, PA, Intraday, Strike):
    """Closes a put credit spread (PCS) on SPY.

    Extended Summary
    ----------------
    This function is used to calculate the debit to close a put credit spread on SPY
    for the given function parameters.

    Parameters
    ----------
    Year : int
        The current year in 4 digit number format.

    DTE : int
        How many full days until expiration for the spread.

    Mark : float
        Current trading price of SPY

    VIX : float
        Current trading price of VIX

    IR : float
        Current trading price/interest rate of the US 10-year treasury bond (^TNX), used to calculate the RFRR

    Delta : float
        The guage of closeness to money for the short and long options

    Width : int
        How many points the strikes are to be spaced out by

    IVF : list
        A list that contains the relationships to map VIX prices to IV for SPY

    PA : list
        A list that contains the coefficients to adjust the mathematical Black-Scholes prices to actual market prices

    Intraday : int
        How far along in the day we are - used to calculate total time until expiration (TTE)

    Strike : int
        Strike for the short position

    Returns
    -------
    Credit : int
        The total amount of credit gained before comissions, fees, and taxes

    Risk : int
        The total amount risked per spread

    Position : boolean
        Updates the Position boolean to be true
    """
    # Total time til expiration that includes intraday
    TTE = DTE + (1 - Intraday/14)

    # IV % of the option based upon VIX pricing on that day and time
    if DTE == 0:
        IV = IVF[0].slope * VIX + IVF[0].intercept
    else:
        IV = IVF[DTE-1].slope * VIX + IVF[DTE-1].intercept

    # Our short and long positions being recalculated using intraday prices
    ShortPut = OC.black_scholes("N/A", Mark, Strike, IR/100, TTE, IV/100, "P")
    LongPut = OC.black_scholes("N/A", Mark, Strike - Width, IR/100, TTE, IV/100, "P")
    
    # # Need moneyness of both options to adjust prices post calculation - this is information
    # # was found by looking at 10 years worth of market data for SPY
    # MoneynessShort = Strike -  Mark
    # MoneynessLong = (Strike -  Width) - Mark

    # # Grab the differences in price from our given SPY data samply
    # PriceDiffShort = PA[Year-2010][DTE-1][0]\
    #     * np.exp(-PA[Year-2010][DTE-1][1] * MoneynessShort**2 * 0.5) / (2*np.pi)
    # PriceDiffLong = PA[Year-2010][DTE-1][0]\
    #     * np.exp(-PA[Year-2010][DTE-1][1] * MoneynessLong**2 * 0.5) / (2*np.pi)

    # # Apply our differential
    # PriceShort = ShortPut.price - PriceDiffShort
    # PriceLong = LongPut.price - PriceDiffLong

    # To neutralize the position we need to sell our long and buy back our short
    Debit = abs(round(LongPut.price - ShortPut.price, 2))

    return Debit

def OpenCCSSPY(Year, DTE, Mark, VIX, IR, Delta, Width, IVF, PA, Intraday):

def CloseCCSSPY(Year, DTE, Mark, VIX, IR, Width, IVF, PA, Intraday, Strike):