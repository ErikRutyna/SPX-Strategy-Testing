import os
import numpy as np
import datetime 
import pricing_test as PT
import backtesting as BT

# Data files of SPY historical information
Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
SPYData = "spy_historical_data.csv"
VIXData = "^VIX_YAHOO_data.csv"
TNXData = "^TNX_YAHOO_data.csv"

SPYData = os.path.join(Folder, SPYData)
VIXData = os.path.join(Folder, VIXData)
TNXData = os.path.join(Folder, TNXData)

DataFiles = [SPYData, VIXData, TNXData]

# Initial Financial Info
InitialBalance =  3000
MaxRisk = 0.1
Delta = [0.25]
ClosingPercent = [0.5]

# Start date - must be after Jan '11 for MWF SPY options
StartDate = datetime.datetime(2011, 1, 3)

# IV Adjustments from the live data
IVAdj = PT.spy_iv_adjust()

for i in range(len(Delta)):
    for j in range(len(ClosingPercent)):
        Conditions = np.array([InitialBalance, MaxRisk, Delta[i], ClosingPercent[j]])
        Results = BT.PCS_SPY(Conditions, StartDate, DataFiles, IVAdj)
        print(("The final balance with backtesting at \u0394-value: {0}"
             " and closing at {1}%% is: ${2}""".format(Delta[i], (100*ClosingPercent[j]), float(Results[0]))))
        print("Investing ${0} into SPY on {1} would yield {2} on December 31, 2020".format(InitialBalance, StartDate, float(Results[7])))