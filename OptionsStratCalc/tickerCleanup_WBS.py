import csv
import datetime
import os
from pathlib import Path
from typing import Final

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