import csv
import os

def tickerDataCleaner_yh(FileName):
    """Cleans up the ticker information from the CSV source file gathered from Yahoo Finance.

    Extended Summary
    ----------------
    This function can be used to remove extraneous information regarding historical
    stock price information for a specific ticker. This cleaned version is used for the 
    option calculator and backtesting programs.

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

    HighCol = 0
    LowCol = 0
    AdjCol = 0
    VolCol = 0

    # Grab the columns of non-needed data
    for i in range(len(rawText[1])):
        if rawText[0][i] == "High":
            HighCol = i
        elif rawText[0][i] == "Low":
            LowCol = i
        elif rawText[0][i] == "Adj Close":
            AdjCol = i
        elif rawText[0][i] == "Volume":
            VolCol = i  

    numRows = len(rawText)
    iRow = numRows - 1

    # Get rid of any "null rows"
    while iRow > 0:
        if "null" in rawText[iRow]:
            del rawText[iRow]
            iRow -= 1
        else:
            del rawText[iRow][VolCol]
            del rawText[iRow][AdjCol]
            del rawText[iRow][LowCol]
            del rawText[iRow][HighCol]
            iRow -= 1

    del rawText[0][VolCol]
    del rawText[0][AdjCol]
    del rawText[0][LowCol]
    del rawText[0][HighCol]
    
    print("Done removing non-ticker rows, onto writing!")
    
    with open(FinalPath, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in rawText:
            writer.writerow(line)

    print("Done writing, please spot check final output file!")
    return