import csv
import os
import scipy
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from datetime import date

def vix_correlator(Folder, OPTData, EODData, VIXData, Style):
    """Runs a regression to find a way to correlate VIX prices to option prices.

    Extended Summary
    ----------------
    This function is used to calculate a relationship between VIX prices and the implied
    volatility of an for a given security at different strike prices. This process uses end 
    of day (EOD) market data to correlate the ImpVol & VIX using the Black-Scholes formula.
    This can be used with both American and European style options.

    Parameters
    ----------
    OptionData : string
        Filename of the csv file where all the EODoption data is held for the security

    EODData : string
        Filename of the csv where all the EoD price data is held for the security

    VIXData : string
        Filename of the csv where all the EOD price data is held for VIX

    Style : character
        The style of the option, either European (E) or American (A)

    Returns
    -------
    coefficients : array
        Array of coefficiencts that fit the option implied volatility to VIX

    Also plots the correlation and data provided using Matplotlib
    """

    # Grab the filepath of the 3 source files needed -  EOD pricing data for security + VIX,
    # as well as the historical option pricing data
    DataFolder = Folder # May have to do some string fuckery with this
    FilePathEOD = EODData + ".csv"
    FilePathVIX = VIXData + ".csv"
    FilePathOPT = OPTData + ".csv"

    FilePathEOD = os.path.join(DataFolder, FilePathEOD)
    FilePathVIX = os.path.join(DataFolder, FilePathVIX)
    FilePathOPT = os.path.join(DataFolder, FilePathOPT)

    # Read in all the CSV Data
    with open(FilePathEOD) as EODcsv:
        EODData = list(csv.reader(EODcsv))

    with open(FilePathVIX) as VIXcsv:
        VIXData = list(csv.reader(VIXcsv))

    with open(FilePathOPT) as OPTcsv:
        OPTData = list(csv.reader(OPTcsv))

    dateCol = 0
    symbCol = 0
    exprCol = 0
    impvCol = 0
    excrCol = 0

    # Grab date & option symbol column, make sure we know what the security is and what
    # column contains dates, option information, and expiration dates
    for iCol in range(len(OPTData[0])):
        if iCol > len(OPTData[0]):
            break
        elif OPTData[0][iCol] == "date":
            dateCol = iCol
        elif OPTData[0][iCol] == "symbol":
            symbCol = iCol
        elif OPTData[0][iCol] == "exdate":
            exprCol = iCol
        elif OPTData[0][iCol] == "impl_volatility":
            impvCol = iCol
        elif OPTData[0][iCol] == "exercise_style":
            excrCol = iCol

    securityName = OPTData[1][symbCol][0:OPTData[1][symbCol].find(" ")]

    # All relevant information for the options contracts
    optionsInfo = []
    VIXIndex = 0
    EODIndex = 0

    # Loop over time using the option data as the earliest starting time
    for iDate in range(1, len(OPTData)):
        tempInfo = []

        # Check to see if the option data has corresponding VIX and closing historical data
        for iCheck in range(VIXIndex, len(VIXData)):
            if VIXData[iCheck][0] == OPTData[iDate][dateCol]:
                VIXCheck = True
                VIXIndex = iCheck
                break
        for iCheck in range(EODIndex, len(EODData)):
            if EODData[iCheck][1] == OPTData[iDate][dateCol]:
                EODCheck = True
                EODIndex = iCheck
                break
        if VIXCheck ^ EODCheck or (VIXCheck == False and EODCheck == False):
            continue

        # Check to see if it is short term option or not
        presentDay = OPTData[iDate][dateCol]
        exprDay = OPTData[iDate][exprCol]
        # Slice it to fit datetime format YEAR 0-3, MONTH 4-5, DAY 6-7
        presentDay = date(int(presentDay[0:4]), int(presentDay[4:6]), int(presentDay[6:8]))
        exprDay = date(int(exprDay[0:4]), int(exprDay[4:6]), int(exprDay[6:8]))

        if (exprDay - presentDay).days > 8:
            continue

        # Build our list for the day
        tempInfo.append(presentDay)
        tempInfo.append(exprDay)
        tempInfo.append((exprDay - presentDay).days)
        tempInfo.append(strike_extractor(OPTData[iDate][symbCol]))
        tempInfo.append(EODData[EODIndex][2])
        tempInfo.append(OPTData[iDate][impvCol])
        tempInfo.append(VIXData[VIXIndex][1])
        tempInfo.append(OPTData[iDate][excrCol])

        # Append it to the big list
        optionsInfo.append(tempInfo)

    IMPV = []
    VIX = []

    for iRow in range(0, len(optionsInfo), 100):
        IMPV.append(optionsInfo[iRow][5])
        VIX.append(optionsInfo[iRow][6])

    volPlot = plt.axes()
    volPlot.xaxis.set_major_locator(plt.MaxNLocator(8))
    volPlot.yaxis.set_major_locator(plt.MaxNLocator(8))
    plt.scatter(VIX, IMPV)
    plt.ylabel("Implied Volatility")
    plt.xlabel("VIX")
    plt.show()
    

def strike_extractor(symbol):
    """Pulls strike price from option symbol.

    Extended Summary
    ----------------
    This function is used to extract the strike price from the long option symbol.
    SPY 20100812P149000 is a put option with expiration date of August 12, 2010 at a strike
    of $149.000. This function would extract the 149.000 information. (This is a completely 
    made up example in terms of dates and prices, but illustrates the point). 

    Parameters
    ----------
    symbol : string
        Full string of the option like in the example in extended summary

    Returns
    -------
    strike : double (float?)
        Pulls the dollar amount of the strike out, adds the decimal and returns the proper
        strike price
    """

    spaceIndex = symbol.find(" ")

    cFlagIndex = symbol[spaceIndex:].find("C")
    pFlagIndex = symbol[spaceIndex:].find("P")

    if cFlagIndex != -1:
        strike = symbol[(spaceIndex + cFlagIndex + 1):]
        strike = strike[0:-2] + "." + strike[-2:]
    elif pFlagIndex != -1:
        strike = symbol[(spaceIndex + pFlagIndex + 1):]
        strike = strike[0:-3] + "." + strike[-3:]

    return strike