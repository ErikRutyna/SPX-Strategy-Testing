from scipy import stats
import optionsCalc as OC
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

def spy_iv_adjust():
    """Runs a linear regression to adjust IV to accurately match market option prices for SPY.

    Extended Summary
    ----------------
    This function is used to enhance a relationship between VIX prices and the implied
    volatility of an for SPY at different strike prices and short term options ([1-7] DTE). 
    This process uses live market data to help the correlatation between the Implied Volatility & VIX.
    This is meant to be used in conjunction with the "impv_rel" function as an enhancement to increase
    accuracy of data for backtesting.


    Returns
    -------
    VIXFit : list
        A list of scypi linear regressions for adjusting short term option implied volaties.
    """
    # All the files where the data for SPY is stored
    F = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    OptionData = "spy_testing_data"
    SecurityPrices = "spy_historical_data"
    VIXPrices = "vix_historical_data"
    LiveData = "spy_live_data.csv"

    # Create linear regression functions that map VIX -> IV for different DTEs, [1-7]
    Fits = OC.impv_rel(F, OptionData, SecurityPrices, VIXPrices, 8)

    # The live option data for SPY from Tastyworks gathered in May '21 
    LiveData = os.path.join(F, LiveData)

    with open(LiveData) as LIVEDATA:
        LIVEDATA = list(csv.reader(LIVEDATA))

    LiveData = np.array(LIVEDATA[1:])
    LiveData = LiveData.astype(np.float)

    # The 10-year bond had return of 1.56% when live data was gathered in May '21
    RFRR = 0.0156
    symbol = "SPY"
    type = "P"
    # List that will contain market data & calculated data in form
    # [Moneyness, quoted/live, BS using IV, BS using VIX]
    PriceCalcs = np.empty([len(LiveData), 4])
    # Translating the live market data into a usable list form
    for iRow in range(len(LiveData)):
        # Temporary list
        Temp = np.array([])

        # Extracting the values out to make it easier to read formulas
        value = LiveData[iRow][0]
        strike = LiveData[iRow][1]
        dte = int(LiveData[iRow][2])
        iv = LiveData[iRow][3]
        quoted = LiveData[iRow][4]
        vix = LiveData[iRow][5]

        # Moneyness
        Moneyness = strike - value
        Temp = np.append(Temp, Moneyness)

        # Quoted/Live
        Temp = np.append(Temp, quoted)

        # Black-Scholes
        tempOpt = OC.black_scholes(symbol, value, strike, RFRR, dte, iv, type)
        Temp = np.append(Temp, tempOpt.price)
        
        # Black-Scholes using VIX
        iv = (Fits[dte-1].slope * vix + Fits[dte-1].intercept)/100
        tempOpt = OC.black_scholes(symbol, value, strike, RFRR, dte, iv, type)
        Temp = np.append(Temp, tempOpt.price)

        # Append back out to global list
        PriceCalcs[iRow] = Temp

    # Sorts & splits the singular list of option prices into ones for each DTE, [1-7]
    SortedPrice = [[] for i in range(7)]
    for iRow in range(len(LiveData)):
        dte = int(LiveData[iRow][2])
        SortedPrice[dte-1].append(PriceCalcs[iRow-1])

    # Linear fit lins that map the adjustments needed to adjust the VIX-calculated -> quoted/live prices
    BSFit = []
    VIXFit = []

    # Loop over the DTE's and check the differences between quoted/live, BS w/ IV & VIX-calcualted
    for iDTE in range(len(SortedPrice)):
        # Everything W.R.T Moneyness (X)
        Moneyness=[]
        QuotedPrice=[]
        BSCalcPrice=[]
        VIXCalcPrice=[]

        # Break out the data 
        Moneyness = np.array(SortedPrice[iDTE])[:, 0]
        QuotedPrice = np.array(SortedPrice[iDTE])[:, 1]
        BSCalcPrice = np.array(SortedPrice[iDTE])[:, 2]
        VIXCalcPrice = np.array(SortedPrice[iDTE])[:, 3]

        BSDiff = (QuotedPrice - BSCalcPrice)
        VIXDiff = (QuotedPrice - VIXCalcPrice)

        BSFit.append(stats.linregress(Moneyness, BSDiff))
        VIXFit.append(stats.linregress(Moneyness, VIXDiff))

        # Plots the difference between difference between prices versus moneyness of the put option
        # titletext = str(iDTE+1) + " DTE"
        # plt.figure()
        # plt.scatter(Moneyness, BSDiff, color="blue")
        # plt.scatter(Moneyness, VIXDiff, color="red")
        # plt.title(titletext)

        # Apply out differences from the linear regression
        BSCalcPriceAdj = BSCalcPrice + (BSFit[iDTE].slope * Moneyness + BSFit[iDTE].intercept)
        VIXCalcPriceAdj = VIXCalcPrice + (VIXFit[iDTE].slope * Moneyness + VIXFit[iDTE].intercept)

        # Sort all the arrays by Moneyness to form a smoother curve
        index = Moneyness.argsort()
        Moneyness = Moneyness[index]
        BSCalcPriceAdj = BSCalcPriceAdj[index]
        VIXCalcPriceAdj = VIXCalcPriceAdj[index]
        QuotedPrice = QuotedPrice[index]

        # Plots the value of the adjusted option compared to the quoted
    #     titletext = str(iDTE+1) + " DTE"
    #     plt.figure()
    #     plt.plot(Moneyness, BSCalcPriceAdj, color="blue")
    #     plt.plot(Moneyness, VIXCalcPriceAdj, color="red")
    #     plt.plot(Moneyness, QuotedPrice, color="black")
    #     plt.title(titletext)

    # plt.show(block=True)
    return VIXFit