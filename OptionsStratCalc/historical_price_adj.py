import optionsCalc as OC
from scipy import optimize
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime
import copy

def historicalPriceAdj():
    """Runs a normal distribution regression to adjust IV to accurately match market option prices for SPY.

    Extended Summary
    ----------------
    This function is used to enhance pricing relationship for SPY at different strike prices based upon
    historical data for short term options ([1-7] DTE). This process uses live market data to help the 
    correlatation between the moneyness of the put options, and the differences in Black-Scholes vs live
    market data. This is meant to be used in conjunction with other relationship functions to improve accuracy
    of backtesting. Tbh this one is kinda shit, but it might work, I dunno


    Returns
    -------
    YearlyAdjFits : list
        A list of coefficients to fit the curve f(x) = C1 * np.exp(-C2 * x**2 * 0.5) / (2*np.pi), where C1 & C2
        are the coefficients. Indexing the list takes form of coeff[YEAR][DTE][coefficient]
    """
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    SPYData = "spy_testing_data"
    SPYPrices = "spy_historical_data"
    VIXPrices = "vix_historical_data"
    HistPutPrices = "spy_options_historical_prices"
    TNX = "^TNX_YAHOO_DATA"

    # IV relationship data
    IVFits = OC.impv_rel(Folder, SPYData, SPYPrices, VIXPrices, 8)

    # Get our historical prices data file
    HistPutPrices = os.path.join(Folder, HistPutPrices + "_data.csv")
    SPYPrices = os.path.join(Folder, SPYPrices+".csv")
    VIXPrices = os.path.join(Folder, VIXPrices+".csv")
    TNX = os.path.join(Folder, TNX+".csv")

    # Read in all 3 data files
    with open(HistPutPrices) as PutPrices:
        HistPutPrices = list(csv.reader(PutPrices))

    with open(SPYPrices) as SPYData:
        SPYPrices = list(csv.reader(SPYData))

    with open(VIXPrices) as VIXData:
        VIXPrices = list(csv.reader(VIXData))

    with open(TNX) as IntRate:
        TNX = list(csv.reader(IntRate))

    # Grab column indices for all the relevant data subsets
    for i in range(len(HistPutPrices[0])):
        if HistPutPrices[0][i] == "date": PutDateCol = i; continue
        elif HistPutPrices[0][i] == "symbol": PutSymbCol = i; continue
        elif HistPutPrices[0][i] == "best_bid": BidCol = i; continue
        elif HistPutPrices[0][i] == "best_offer": AskCol = i; continue
        elif HistPutPrices[0][i] == "exdate": ExprCol = i; continue

    for i in range(len(SPYPrices[0])):
        if SPYPrices[0][i] == "Date": SPYDateCol = i; continue
        elif SPYPrices[0][i] == "Open": SPYOpenCol = i; continue
        elif SPYPrices[0][i] == "Close": SPYCloseCol = i; continue

    for i in range(len(VIXPrices[0])):
        if VIXPrices[0][i] == "Date": VIXDateCol = i; continue
        elif VIXPrices[0][i] == "vixo": VIXOpenCol = i; continue
        elif VIXPrices[0][i] == "vix": VIXCloseCol = i; continue

    for i in range(len(TNX[0])):
        if TNX[0][i] == "Date": TNXDateCol = i; continue
        elif TNX[0][i] == "Open": TNXOpenCol = i; continue
        elif TNX[0][i] == "Close": TNXCloseCol = i; continue
        
    # Convert the lists to arrays for a slight increase in speed
    HistPutPrices = np.array(HistPutPrices[1:])
    SPYPrices = np.array(SPYPrices[1:])
    VIXPrices = np.array(VIXPrices[1:])
    TNX = np.array(TNX[1:])


    # Setup the list of lists of lists containing the information
    # Data[year][dte] -> [0] => price difference 
    # Data[year][dte] -> [1] => moneyness
    PriceAdjustments = [[] for _ in range(11)]

    # Adds the second-nesting for DTE, and third for the 2 lists of data
    for i in range(len(PriceAdjustments)):
        Temp = ([[] for _ in range(4)])
        for j in range(len(Temp)):
            Temp[j] = [[],[]]
        PriceAdjustments[i] = Temp

    MoneynessLimit = 7 # Maximum Moneyness difference allowed

    # Normal distribution curve-fit, probably the closest generic-like curve for the data
    def normCurve(x, C1, C2):
        return (C1 * np.exp(-C2 * x**2 * 0.5) / (2*np.pi))
    # normCurve = np.vectorize(normCurve)

    # Trimming list like what I did for IV correlation
    TrimMultiplier = [4, 3, 2.5, 2, 1.5]

    # Dates are always sequential, can use last index to save iteration time
    LastIndexSPY = 0
    LastIndexVIX = 0
    LastIndexTNX = 0

    # Grab the close to ATM options' moneyness and their respective prices
    for index, CurrentDay in enumerate(HistPutPrices):

        CurrDate = datetime.datetime(int(HistPutPrices[index][PutDateCol][0:4]), \
            int(HistPutPrices[index][PutDateCol][4:6]), int(HistPutPrices[index][PutDateCol][6:8]))
        ExprDate = datetime.datetime(int(HistPutPrices[index][ExprCol][0:4]), \
            int(HistPutPrices[index][ExprCol][4:6]), int(HistPutPrices[index][ExprCol][6:8]))
        DTE = (ExprDate - CurrDate).days

        # Only working w/ short term derivatives so skip all > weeklys
        if DTE > 4 or DTE == 0:
            continue

        # Grab out open & close prices for the day and average them to find a middle ground
        for i in range(LastIndexSPY, len(SPYPrices)):
            if CurrentDay[0] == SPYPrices[i][SPYDateCol]:
                SPYAvg = (float(SPYPrices[i][SPYOpenCol]) + float(SPYPrices[i][SPYCloseCol]))/2
                LastIndexSPY = i
                break

        for i in range(LastIndexVIX, len(VIXPrices)):
            if CurrentDay[0] == VIXPrices[i][VIXDateCol]:
                VIXAvg = (float(VIXPrices[i][VIXOpenCol]) + float(VIXPrices[i][VIXCloseCol]))/2
                LastIndexVIX = i
                break

        for i in range(LastIndexTNX, len(TNX)):
            TNXDate = TNX[i][TNXDateCol]
            TNXDate = TNXDate[0:4] + TNXDate[5:7] + TNXDate[8:10]
            if CurrentDay[0] == TNXDate:
                TNXAvg = (float(TNX[i][TNXOpenCol]) + float(TNX[i][TNXCloseCol]))/2
                LastIndexTNX = i
                break

        PIndex = CurrentDay[PutSymbCol][5:].index("P")
        StartIndex = PIndex + 6
        Strike = float(HistPutPrices[index][PutSymbCol][StartIndex:StartIndex+5])/100
        Moneyness = (Strike - SPYAvg) 
        Price = (float(HistPutPrices[index][BidCol]) + float(HistPutPrices[index][AskCol]))/2


        # Check condition met, find DTE along with all the pricing information
        if abs(Moneyness) < MoneynessLimit:

            # Now find Black-Scholes W/ IV and price mis-match between calculated and market
            IV = IVFits[DTE-1].slope * VIXAvg + IVFits[DTE-1].intercept
            MyPut = OC.black_scholes("SPY", SPYAvg, Strike, TNXAvg/100, DTE, IV/100, "P")

            # Difference between the two costs
            PriceDiff = MyPut.price - Price

            # Append the current day's options to the global list
            PriceAdjustments[int(HistPutPrices[index][PutDateCol][2:4])-10][DTE-1][0].append(abs(PriceDiff))
            PriceAdjustments[int(HistPutPrices[index][PutDateCol][2:4])-10][DTE-1][1].append(Moneyness)

    # Don't have 2010 market data, so just assume that 2011 is the same
    PriceAdjustments[0] = PriceAdjustments[1]

    # Save a copy of the data for plotting
    HeldData = copy.deepcopy(PriceAdjustments)

    YearlyAdjFits = [[] for i in range(12)]
    for i in range(len(YearlyAdjFits)):
        Temp = [[] for j in range(4)]
        YearlyAdjFits[i] = Temp

    for iYear in range(len(PriceAdjustments)):
        for iDTE in range(len(PriceAdjustments[iYear])):
            for iFit in range(len(TrimMultiplier)):

                # Fit the function
                X = np.array(PriceAdjustments[iYear][iDTE][1])
                Y = np.array(PriceAdjustments[iYear][iDTE][0])
                coeff, _ = optimize.curve_fit(normCurve, X, Y, p0=[0.1, 1], maxfev=1000000)

                # Apply our pseudo-trimming/overfitting methodology
                for i in range(len(PriceAdjustments[iYear][iDTE][0])-1, -1, -1):
                    Cutoff = TrimMultiplier[iFit] * normCurve(PriceAdjustments[iYear][iDTE][1][i], coeff[0], coeff[1])
                    if PriceAdjustments[iYear][iDTE][0][i] > (Cutoff):
                        del PriceAdjustments[iYear][iDTE][1][i]
                        del PriceAdjustments[iYear][iDTE][0][i]

            # One final regression to get the best fit and slot it into out return list
            FinalFit, _ = optimize.curve_fit(normCurve, PriceAdjustments[iYear][iDTE][1], PriceAdjustments[iYear][iDTE][0])
            X = np.linspace(min(PriceAdjustments[iYear][iDTE][1]), max(PriceAdjustments[iYear][iDTE][1]), 100)
            Y = normCurve(X, FinalFit[0], FinalFit[1])

            YearlyAdjFits[iYear][iDTE] = FinalFit
            TitleText = "Price adjustments for the year {0} and {1} DTE".format(2010+iYear, iDTE+1)
            # Plot our results
            plt.figure()
            plt.scatter(HeldData[iYear][iDTE][1], HeldData[iYear][iDTE][0], color="black")
            plt.plot(X, Y, color="red")
            plt.title(TitleText)

        plt.show(block=True)
    return YearlyAdjFits