import math
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.function_base import linspace
from scipy import stats
from pathlib import Path
from datetime import date

def black_scholes(symbol, value, strike, interest, time, IV, type):
    """Calculates the fair market value of an option using the Black-Scholes formula.

    Extended Summary
    ----------------
    This function is used to calculate the fair market pricing for a derivative of a security
    using the Black-Scholes formula for a given strike price and time until expiration. This 
    formula works for both Calls and Puts, but does assume that that options are European style.

    Parameters
    ----------
    symbol : string
        Symbol/Ticker for the underyling security

    price : float
        Current value of the underlying security

    strike : float 
        Strike price for the option

    interest : float 
        Risk-free rate of return measured using the 10-year US bond annual rate of return

    time : float
        Number of days until expiration which is converted into years in the formula

    IV : float
        Implied volatility of the derivative contract

    Type : char
        Call or Put flag - is only either P or F

    Returns
    -------
    contract : OPTION
        Information about the option contract including basic information as well as the greeks.
    """
    option_info = OPTION()
    # Formula for Black-Scholes --> https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
    d1 = 1 / (IV * math.sqrt(time/365)) * (np.log(value/strike) + (interest + IV**2/2)*(time/365))
    #d1 = 0.4342
    d2 = d1 - IV*math.sqrt(time/365)
    #d2 = 0.2928
    if type == "P":
        opt_cost = stats.norm.cdf(-d2) * strike * math.exp(-interest * time/365) - stats.norm.cdf(-d1) * value
        delta = stats.norm.cdf(d1) - 1
        theta = -(strike * stats.norm.pdf(d1) * IV) / (2 * math.sqrt(time/365)) + interest * strike * math.exp(-interest * time / 365) * stats.norm.cdf(-d2)
    elif type == "C":
        opt_cost = stats.norm.cdf(d1) * value - stats.norm.cdf(d2) * strike * math.exp(-interest * time/365)
        delta = stats.norm(d1) 
        theta = -(strike * stats.norm.pdf(d1) * IV) / (2 * math.sqrt(time/365)) - interest * strike * math.exp(-interest*time/365) * stats.norm.cdf(d2)

    gamma = stats.norm.pdf(d1) / (value * IV * math.sqrt(time/365))
    vega = value * stats.norm.pdf(d1) * math.sqrt(time/365)

    option_info.symbol = symbol
    option_info.type = type
    option_info.price = round(opt_cost, 2)
    option_info.strike = strike
    option_info.dte = time
    option_info.delta = round(delta, 3)
    option_info.gamma = gamma
    option_info.vega = round((vega / 100), 4)
    option_info.theta = round((theta / 365), 4)

    return option_info
  
def impv_rel(Folder, OPTData, EODData, VIXData, maxdte):
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
        Filename w/o extension of the csv file where all the EODoption data is held for the security

    EODData : string
        Filename w/o extension of the csv where all the EoD price data is held for the security

    VIXData : string
        Filename w/o extension of the csv where all the EOD price data is held for VIX

    maxdte : int
        Maximum number of days until expiration for any option present in data

    Returns
    -------
    bestFits : list
        List of best fit lines for corresponding days until expiration

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

        strike = float(strike_extractor(OPTData[iDate][symbCol]))

        DTE = maxdte
        Diff2Strike = 15
        # Check to see if the option present fits our criteria of days to expiration and difference to strike
        if ((exprDay - presentDay).days > DTE and abs(strike - float(EODData[EODIndex][2])) < Diff2Strike):
            continue

        # Build our list for the day
        tempInfo.append(presentDay)
        tempInfo.append(exprDay)
        tempInfo.append((exprDay - presentDay).days)
        tempInfo.append(strike)
        tempInfo.append(float(EODData[EODIndex][2]))
        tempInfo.append(100*float(OPTData[iDate][impvCol]))
        tempInfo.append(float(VIXData[VIXIndex][1]))

        # Append it to the big list
        optionsInfo.append(tempInfo)

    # Pull out VIX and implied volatility
    IMPV = [[] for i in range(DTE-1)]
    VIX = [[] for i in range(DTE-1)]
 

    # Filter out the few hundred thousand into a few thousand
    for iRow in range(0, len(optionsInfo), 100):
        IMPV[optionsInfo[iRow][2]-1].append(optionsInfo[iRow][5])
        VIX[optionsInfo[iRow][2]-1].append(optionsInfo[iRow][6])

    # Make our linear regressions, then remove outliers - runs a few times to trim off fat
    # Could probably improve this method of multi-regression, but for now it "works"
    trimMultiplier = [5, 3, 2, 1.5, 1.33]

    for iReg in range(len(trimMultiplier)):
        bestFits = [[] for i in range(DTE-1)]
        for iRow in range(len(IMPV)):
            bestFits[iRow] = stats.linregress(VIX[iRow], IMPV[iRow])

        # Define out outliers as >2x the regression value
        for iRow in range(len(VIX)):
            for iCol in range(len(VIX[iRow])-1, -1, -1):
                val = trimMultiplier[iReg] * (bestFits[iRow].slope * VIX[iRow][iCol] + bestFits[iRow].intercept)
                if (IMPV[iRow][iCol] > val):
                    del(IMPV[iRow][iCol])
                    del(VIX[iRow][iCol])

    # One final update to the best fit lines
    for iRow in range(len(IMPV)):
            bestFits[iRow] = stats.linregress(VIX[iRow], IMPV[iRow])

    # Then plot it
    for iRow in range((len(IMPV))):
        titletext = securityName + " puts' IV with %s DTE" % str(iRow+1)
        X = linspace(min(VIX[iRow]), max(VIX[iRow]), len(VIX[iRow]))
        Y = []
        for i in range(len(VIX[iRow])):
            Y.append(bestFits[iRow].slope * X[i] + bestFits[iRow].intercept)
        plt.figure()
        plt.plot(VIX[iRow], IMPV[iRow],"o",color="black")
        plt.plot(X, Y, color="red")
        plt.title(titletext)
        plt.xlabel("VIX Price")
        plt.ylabel("Implied Volatility")

    plt.show(block=True)

    return bestFits

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
 
def tickerDataCleaner(Ticker, FileName):
    """Cleans up the ticker information from the CSV source file.

    Extended Summary
    ----------------
    This function can be used to remove extraneous information regarding historical
    option information for a specific ticker. This cleaned version is used for the 
    option calculator and backtester.

    Parameters
    ----------
    Ticker : string
        The shortcode string for the security

    FilePath : string
        The filepath to the source CSV containing the security and derivatives information

    "Returns"
    -------
    Nothing --- saves a file in the same directory as input files that is a "cleaned" CSV
    """


    # Get our full filepath
    FilePath = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    SourceFile = FileName + ".csv"
    CSVPath = os.path.join(FilePath, SourceFile)
    
    # Get our final filepath
    FinalFile = FileName + "DATA.csv"
    FinalPath = os.path.join(FilePath, FinalFile)

    # Grab the CSV from the fixed Master Data directory, load it in and get ready to clean it
    with open(CSVPath) as tickerCSV:
        rawText = list(csv.reader(tickerCSV))

    symbolCol = 0
    # Find out which column is our matching symbol
    for iSym in range(len(rawText[1])):
        if rawText[0][iSym] == 'symbol':
            symbolCol = iSym

    
    impVolCol = 0
    # Find out which column is our implied volatility
    for iVol in range(len(rawText[1])):
        if rawText[0][iVol] == 'impl_volatility':
            impVolCol = iVol

    # Generate strings for the two long names of the options to be checked
    contractName1 = Ticker + " 1"
    contractName2 = Ticker + " 2"

    iRow = len(rawText) - 1
    # If the row of the text is not SPY, delete the row
    # Or if the row is empty then delete the row
    # Save the initial line at row 0 for the information on formatting
    while iRow > 0:
        #print(rawText[iRow][symbolCol])
        if ((contractName1 in rawText[iRow][symbolCol]) or (contractName2 in rawText[iRow][symbolCol])) and (bool(rawText[iRow][impVolCol])):
            iRow -= 1
        else:
            del rawText[iRow]
            iRow -= 1

    print("Done removing non-ticker rows, onto writing!")
    
    with open(FinalPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in rawText:
            writer.writerow(line)

    print("Done writing, please spot check final output file!")

class OPTION:
    def __init__(self):
        self.symbol = None
        self.type = None
        self.price = None
        self.strike = None
        self.dte =  None
        self.delta = None
        self.gamma = None
        self.vega = None
        self.theta = None

    def __str__(self):
        if self.type == "C":    
            return (self.symbol + " call option at a strike of $" + str(self.strike) + " with " + str(self.dte) + " days until expiration has a value of $" + str(self.price))
        elif self.type == "P":
            return (self.symbol + " put option at a strike of $" + str(self.strike) + " with " + str(self.dte) + " days until expiration has a value of $" + str(self.price))