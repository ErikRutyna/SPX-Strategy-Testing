import csv
import datetime
import os
import numpy as np
import pandas as pd
from multiprocessing import Pool

def tickerDataCleaner_iv(Ticker, FileName):
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
    FinalFile = FileName + "_data.csv"
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

def tickerDataCleaner_price(Ticker, FileName):
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
    FinalFile = FileName + "_data.csv"
    FinalPath = os.path.join(FilePath, FinalFile)

    # Grab the CSV from the fixed Master Data directory, load it in and get ready to clean it
    with open(CSVPath) as tickerCSV:
        rawText = list(csv.reader(tickerCSV))

    # Find out which column is our matching symbol
    for iSym in range(len(rawText[1])):
        if rawText[0][iSym] == 'symbol': symbolCol = iSym; break

    # Generate strings for the two long names of the options to be checked
    contractName1 = Ticker + " 1"
    contractName2 = Ticker + " 2"

    Length =  len(rawText) - 1
    # If the row of the text is not SPY, delete the row
    # Or if the row is empty then delete the row
    # Save the initial line at row 0 for the information on formatting
    for iRow in range(Length, -1):
        if iRow == 0:
            continue
        elif ((contractName1 in rawText[iRow][symbolCol]) or (contractName2 in rawText[iRow][symbolCol])):
            continue
        else:
            del rawText[iRow]

    print("Done removing non-ticker rows, onto writing!")
    
    with open(FinalPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in rawText:
            writer.writerow(line)

    print("Done writing, please spot check final output file!")

    # """Cleans up the ticker information from the CSV source file.

    # Extended Summary
    # ----------------
    # This function can be used to remove extraneous information regarding historical
    # option information for a specific ticker. This cleaned version is used for the 
    # option calculator and backtester - only to be used on SPY calls file.

    # Parameters
    # ----------
    # Ticker : string
    #     The shortcode string for the security

    # FilePath : string
    #     The filepath to the source CSV containing the security and derivatives information

    # "Returns"
    # -------
    # Nothing --- saves a file in the same directory as input files that is a "cleaned" CSV
    # """


    # # Get our full filepath
    # FilePath = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    # SourceFile = FileName + ".csv"
    # CSVPath = os.path.join(FilePath, SourceFile)
    
    # # Get our final filepath
    # FinalFile = FileName + "DATA.csv"
    # FinalPath = os.path.join(FilePath, FinalFile)

    # # Grab the CSV from the fixed Master Data directory, load it in and get ready to clean it
    # with open(CSVPath) as tickerCSV:
    #     rawText = list(csv.reader(tickerCSV))

    # symbolCol = 0
    # # Find out which column is our matching symbol
    # for iSym in range(len(rawText[1])):
    #     if rawText[0][iSym] == 'symbol':
    #         symbolCol = iSym

    
    # impVolCol = 0
    # # Find out which column is our implied volatility
    # for iVol in range(len(rawText[1])):
    #     if rawText[0][iVol] == 'impl_volatility':
    #         impVolCol = iVol

    # # Generate strings for the two long names of the options to be checked
    # contractName1 = Ticker + " 1"
    # contractName2 = Ticker + " 2"

    # iRow = len(rawText) - 1
    # # If the row of the text is not SPY, delete the row
    # # Or if the row is empty then delete the row
    # # Save the initial line at row 0 for the information on formatting
    # while iRow > 0:
    #     #print(rawText[iRow][symbolCol])
    #     if ((contractName1 in rawText[iRow][symbolCol]) or (contractName2 in rawText[iRow][symbolCol])) and (bool(rawText[iRow][impVolCol])):
    #         iRow -= 1
    #     else:
    #         del rawText[iRow]
    #         iRow -= 1

    # print("Done removing non-ticker rows, onto writing!")
    
    # with open(FinalPath, 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     for line in rawText:
    #         writer.writerow(line)

    # print("Done writing, please spot check final output file!")

def SPY_SPX_data_extractor(Filename):
    """Extracts the historical options chain for SPY and SPX.

    Extended Summary
    ----------------
    This function can be used to create historical options chain for short DTE (< 15 DTE) and
    small close to the money Moneyness < 35 for SPY and Moneyness < 350 for SPX from the given
    historical data file.

    Parameters
    ----------

    Filename : string
        The filename of the source CSV with the entire historical options chain.

    "Returns"
    -------
    Nothing --- saves a file in the same directory as input files that is a "cleaned/reduced" CSV
        that has only the information we want
    """
    # Data directory
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"
    # Location of the file
    Filename = os.path.join(Folder, Filename)

    # Open/load in the CSV and read it all into memory (yikes!)
    with open(Filename) as FileIn:
        RawChain = list(csv.reader(FileIn))

    # Header line that contains all the column information
    Header = np.array(RawChain[0])
    SymCol = int(np.where(Header == "symbol")[0])
    FlgCol = int(np.where(Header == "cp_flag")[0])
    BidCol = int(np.where(Header == "best_bid")[0])
    OfrCol = int(np.where(Header == "best_offer")[0])
    VolCol = int(np.where(Header == "impl_volatility")[0])
    DelCol = int(np.where(Header == "delta")[0])

    # The four categories
    SPXCalls = []
    SPXPuts = []
    SPYCalls = []
    SPYPuts = []

    for i in range(len(RawChain)-1, -1, -1):
        if i == 0: break

        Symbol = RawChain[i][SymCol][0:5]

        # Delete any row that doesnt contain needed information, or is the wrong ticker
        if (not RawChain[i][BidCol]) or (not RawChain[i][BidCol]) or (not RawChain[i][OfrCol])\
            or (not RawChain[i][VolCol]) or (not RawChain[i][DelCol])\
                or ((not "SPY" in Symbol) and (not "SPXW" in Symbol)):
            del RawChain[i]; continue

        # Sort out the data into puts and calls for the different chains
        if "SPXW" in Symbol:
            if "P" in RawChain[i][FlgCol]:
                 SPXPuts.append(RawChain[i])
            else:
                SPXCalls.append(RawChain[i])
                
        elif "SPY" in Symbol:
            if "P" in RawChain[i][FlgCol]:
                SPYPuts.append(RawChain[i])
            else:
                SPYCalls.append(RawChain[i])

    print("Done cleaning and sorting, now writing")
    # def parallelframe(OptionsChain, Cleaner):
    #     SplitChain = np.array_split(OptionsChain, 4)
    #     pool = Pool(4)
    #     CombinedChain = pd.concat(pool.map(ParallelCleaner, SplitChain))
    #     pool.close()
    #     pool.join()
    #     return CombinedChain

    # Turn it into an array - get rid of the old list
    SPXCallPath = os.path.join(Folder, "SPXCallsChain.csv")
    SPXPutPath = os.path.join(Folder, "SPXPutsChain.csv")
    SPYPutPath = os.path.join(Folder, "SPYCallsChain.csv")
    SPYCallPath = os.path.join(Folder, "SPYPutsChain.csv")


    
    print("Done sorting - on to writing")

    with open(SPXCallPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in SPXCalls:
            writer.writerow(line)

    with open(SPXPutPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in SPXPuts:
            writer.writerow(line)

    with open(SPYPutPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in SPYCalls:
            writer.writerow(line)

    with open(SPYCallPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in SPYPuts:
            writer.writerow(line)

    return

def ParallelCleaner(RawOptChain):
    Header = np.array(RawOptChain[0])
    SymCol = int(np.where(Header == "symbol")[0])
    ExpCol = int(np.where(Header == "exdate")[0])
    FlgCol = int(np.where(Header == "cp_flag")[0])
    BidCol = int(np.where(Header == "best_bid")[0])
    OfrCol = int(np.where(Header == "best_offer")[0])
    VolCol = int(np.where(Header == "impl_volatility")[0])
    DelCol = int(np.where(Header == "delta")[0])

    for i in range(len(RawOptChain)-1, -1, -1):
        Symbol = RawOptChain[i][SymCol][0:5]

        # Delete any row that doesnt contain needed information, or is the wrong ticker
        if (not RawOptChain[i][BidCol]) or (not RawOptChain[i][BidCol]) or (not RawOptChain[i][OfrCol])\
            or (not RawOptChain[i][VolCol]) or (not RawOptChain[i][DelCol])\
                or ((not "SPY" in Symbol) and (not "SPXW" in Symbol)):
            del RawOptChain[i]
    return RawOptChain

def miscCallsCleaner():
    """This only should be used once, ignore me otherwise.
    """
    Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    SPYPrices = "spy_historical_data"
    VIXPrices = "vix_historical_data"
    SPYCalls = "spy_calls_data"

    # Grab the filepath of the 3 source files needed -  EOD pricing data for security + VIX,
    # as well as the historical option pricing data
    DataFolder = Folder # May have to do some string fuckery with this
    FilePathPrice = SPYPrices + ".csv"
    FilePathVIX = VIXPrices + ".csv"
    FilePathCalls = SPYCalls + ".csv"

    FilePathPrice = os.path.join(DataFolder, FilePathPrice)
    FilePathVIX = os.path.join(DataFolder, FilePathVIX)
    FilePathCalls = os.path.join(DataFolder, FilePathCalls)
    FinalPath = os.path.join(DataFolder, SPYCalls + "_reduced.csv")

    # Read in all the CSV Data
    with open(FilePathCalls) as Callcsv:
        CallData = list(csv.reader(Callcsv))

    dateCol = 0
    exprCol = 0

    # Grab date & option symbol column, make sure we know what the security is and what
    # column contains dates, option information, and expiration dates
    for iCol in range(len(CallData[0])):
        if CallData[0][iCol] == "date": dateCol = iCol; continue
        elif CallData[0][iCol] == "symbol": symbCol = iCol; continue
        elif CallData[0][iCol] == "exdate": exprCol = iCol; continue
        elif CallData[0][iCol] == "impl_volatility": impvCol = iCol; continue

    for iRow in range(len(CallData)-1, -1, -1):
        if iRow == 0:
            break
        
        presentDay = CallData[iRow][dateCol]
        exprDay = CallData[iRow][exprCol]
        
        # Slice it to fit datetime format YEAR 0-3, MONTH 4-5, DAY 6-7
        presentDay = datetime.date(int(presentDay[0:4]), int(presentDay[4:6]), int(presentDay[6:8]))
        exprDay = datetime.date(int(exprDay[0:4]), int(exprDay[4:6]), int(exprDay[6:8]))
        
        DTE = (exprDay - presentDay).days
        
        if DTE > 8:
            del CallData[iRow]

    
    with open(FinalPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in CallData:
            writer.writerow(line)
    return