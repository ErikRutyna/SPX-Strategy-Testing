import csv
import os
from pathlib import Path

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

    """Cleans up the ticker information from the CSV source file.

    Extended Summary
    ----------------
    This function can be used to remove extraneous information regarding historical
    option information for a specific ticker. This cleaned version is used for the 
    option calculator and backtester - only to be used on SPY calls file.

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
