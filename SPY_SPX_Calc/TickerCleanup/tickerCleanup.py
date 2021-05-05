from pathlib import Path
import csv
import os
import pandas as pd
import numpy as np
from multiprocessing import Pool

def tickerDataCleaner(Ticker, Extension):
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

    Returns
    -------
    FilePath : string
        The same filepath location is the cleaned and edited CSV
    """


    # Get our full Filepath
    FilePath = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
    CSVPath = os.path.join(FilePath, Extension)
    

    # Grab the CSV from the fixed Master Data directory, load it in and get ready to clean it
    with open(CSVPath) as tickerCSV:
        rawText = list(csv.reader(tickerCSV))

    symbolCol = 0
    # Find out which column is our matching symbol
    for iSym in range(len(rawText[1])):
        if rawText[0][iSym] == 'ticker':
            symbolCol = iSym
        
    iRow = len(rawText) - 1
    # If the row of the text is not SPY, delete the row
    # Save the initial line at row 0 for the information on formatting
    while iRow > 1:
        #print(rawText[iRow][symbolCol])
        if rawText[iRow][symbolCol] != Ticker:
            del rawText[iRow]
            iRow -= 1
        else:
            iRow -= 1

    print("Done removing non-ticker rows, onto writing!")

    # Write the text back to a cleaned CSV
    with open(CSVPath, "wb") as cleanedTicker:
        writer = csv.writer(cleanedTicker, delimiter=',')
        for line in rawText:
            writer.writerow(line) 