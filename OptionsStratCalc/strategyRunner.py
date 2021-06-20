import os
import numpy as np
import datetime 
import backtesting_strats as BT

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
Delta = [0.3]
ClosingPercent = [0.75]

# Start date - must be after Jan '11 for MWF SPY options
# Earliest date is 2010-01-04
StartDate = datetime.datetime(2020, 1, 3)

for i in range(len(Delta)):
    for j in range(len(ClosingPercent)):
        Conditions = np.array([InitialBalance, MaxRisk, Delta[i], ClosingPercent[j]])
        Results = BT.PCS_SPY(Conditions, StartDate, DataFiles)

print("The final profit from backtesting with a \u0394-value: {0} and closing at {1}% is: ${2}".format(Delta[i], (100*ClosingPercent[j]), float(Results[0])))
print("The total number of trades is: {0}".format(int(Results[1])))
print("The total amount of spreads traded is: {0}".format(int(Results[8])))
print("The total amount spent in comissions is: {0}".format(int(Results[2])))
print("The total number of day trades is: {0}".format(int(Results[3])))
print("The number of trades fully lost is: {0}".format(int(Results[4])))
print("The number of trades partially lost is: {0}".format(int(Results[5])))
print("The total amount spent on taxes is: {0}".format(float(Results[6])))
print("Investing ${0} into SPY on 12/31/2010 would yield ${1} on December 31, 2020".format(InitialBalance, float(Results[7])))