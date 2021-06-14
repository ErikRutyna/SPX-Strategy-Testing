import spy_price_adjuster as PA
import optionsCalc as OC
import tickerCleanup_WBS as TCW
from scipy import stats
import csv
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime

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
    Temp = ([[] for _ in range(7)])
    for j in range(len(Temp)):
        Temp[j] = [[],[]]
    PriceAdjustments[i] = Temp

iDate = 1
DateSkip = 0 # Factor used to increment loop and skip over data we don't need
MoneynessLimit = 15 # Maximum Moneyness difference allowed

# Dates are always sequential, can use last index to save iteration time
LastIndexSPY = 0
LastIndexVIX = 0
LastIndexTNX = 0

# Grab the close to ATM options' moneyness and their respective prices
for index, CurrentDay in enumerate(HistPutPrices):

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

        CurrDate = datetime.datetime(int(HistPutPrices[index][PutDateCol][0:4]), \
            int(HistPutPrices[index][PutDateCol][4:6]), int(HistPutPrices[index][PutDateCol][6:8]))
        ExprDate = datetime.datetime(int(HistPutPrices[index][ExprCol][0:4]), \
            int(HistPutPrices[index][ExprCol][4:6]), int(HistPutPrices[index][ExprCol][6:8]))
        DTE = (ExprDate - CurrDate).days

        # Only working w/ short term derivatives so skip all > weeklys
        if DTE > 7 or DTE == 0:
            continue

        # Now find Black-Scholes W/ IV and price mis-match between calculated and market
        IV = IVFits[DTE-1].slope * VIXAvg + IVFits[DTE-1].intercept
        MyPut = OC.black_scholes("SPY", SPYAvg, Strike, TNXAvg/100, DTE, IV/100, "P")

        # Difference between the two costs
        PriceDiff = MyPut.price - Price

        # Append the current day's options to the global list
        PriceAdjustments[int(HistPutPrices[index][PutDateCol][2:4])-10][DTE-1][0].append(PriceDiff)
        PriceAdjustments[int(HistPutPrices[index][PutDateCol][2:4])-10][DTE-1][1].append(Moneyness)

# Don't have 2010 market data, so just assume that 2011 is the same
PriceAdjustments[0] = PriceAdjustments[1]


YearlyAdjFits = [[] for i in range(12)]

for iYear in range(len(PriceAdjustments)):
    for iDTE in range(len(PriceAdjustments[iYear])):

        TempFit = stats.linregress(PriceAdjustments[iYear][iDTE][1], PriceAdjustments[iYear][iDTE][0])
        YearlyAdjFits[iYear].append(TempFit)

        TitleText = "Price adjustments for the year {0} and {1} DTE".format(2010+iYear, iDTE+1)
        # Plot our results
        plt.figure()
        plt.scatter(PriceAdjustments[iYear][iDTE][1], PriceAdjustments[iYear][iDTE][0])
        plt.title(TitleText)

    plt.show(block=True)
print("Done")