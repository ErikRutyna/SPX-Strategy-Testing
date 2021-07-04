import os
import numpy as np
import datetime 
import backtesting_strats_spy as BTSPY
import backtesting_strats_spx as BTSPX
import warnings

warnings.filterwarnings("ignore")

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
MaxRiskTrade = 500/3000
Delta = [0.15, 0.20, 0.25, 0.3, 0.35, 0.4]
Scaling = ["width", "contracts"]
MaxRiskTotal = 20000

# Start date - must start in/after Jan 6 '17 for MWF SPY options due to limite ddata
# Good dates to test are on (YEAR-MONTH-DAY):
# 2020 - 1 - 2
# 2016 - 1 - 5
# 2017 - 1 - 6
StartDate = datetime.datetime(2016, 1, 5)


for i in range(len(Delta)):
    for j in range(len(Scaling)):

        print("===== Now testing PCS =====")
        Conditions = np.array([InitialBalance, MaxRiskTrade, Delta[i], MaxRiskTotal])
        Results = BTSPX.PCS_SPX(Conditions, StartDate, Scaling[j])
        print("The final profit with \u0394 = {0} and scaling via ".format(Delta[i])\
             + Scaling[j] + " is: ${0}".format(round(float(Results[0]),2)))
        print("The average return on collateral per trade is: {0}%".format(round(float(Results[9]),4)))
        print("The total number of trades done: {0}".format(int(Results[1])))
        print("The total number of historical trades is: {0}".format(int(Results[1]) - int(Results[10])))
        print("The total number of trades simulated: {0}".format(int(Results[10])))
        print("The total amount of spreads traded is: {0}".format(int(Results[2])))
        print("The number of trades fully won is: {0}".format(int(Results[3])))
        print("The number of trades partially won is: {0}".format(int(Results[4])))
        print("The number of trades partially lost is: {0}".format(int(Results[5])))
        print("The number of trades fully lost is: {0}".format(int(Results[6])))
        print("The total amount spent on taxes is: ${0}".format(round(float(Results[7]),2)))
        print("The total amount spent in comissions is: ${0}".format(round(float(Results[8]), 2)))
        print("\n")

        print("\n ===== Now testing CCS =====")
        Conditions = np.array([InitialBalance, MaxRiskTrade, Delta[i], MaxRiskTotal])
        Results = BTSPX.CCS_SPX(Conditions, StartDate, Scaling[j])
        print("The final profit with \u0394 = {0} and scaling via ".format(Delta[i])\
             + Scaling[j] + " is: ${0}".format(round(float(Results[0]),2)))
        print("The average return on collateral per trade is: {0}%".format(round(float(Results[9]),4)))
        print("The total number of trades done: {0}".format(int(Results[1])))
        print("The total number of historical trades is: {0}".format(int(Results[1]) - int(Results[10])))
        print("The total number of trades simulated: {0}".format(int(Results[10])))
        print("The total amount of spreads traded is: {0}".format(int(Results[2])))
        print("The number of trades fully won is: {0}".format(int(Results[3])))
        print("The number of trades partially won is: {0}".format(int(Results[4])))
        print("The number of trades partially lost is: {0}".format(int(Results[5])))
        print("The number of trades fully lost is: {0}".format(int(Results[6])))
        print("The total amount spent on taxes is: ${0}".format(round(float(Results[7]),2)))
        print("The total amount spent in comissions is: ${0}".format(round(float(Results[8]), 2)))
        print("\n")

        print("\n ===== Now testing ICS =====")
        Conditions = np.array([InitialBalance, MaxRiskTrade, Delta[i], MaxRiskTotal])
        Results = BTSPX.ICS_SPX(Conditions, StartDate, Scaling[j])
        print("The final profit with \u0394 = {0} and scaling via ".format(Delta[i])\
             + Scaling[j] + " is: ${0}".format(round(float(Results[0]),2)))
        print("The average return on collateral per trade is: {0}%".format(round(float(Results[9]),4)))
        print("The total number of trades done: {0}".format(int(Results[1])))
        print("The total number of historical trades is: {0}".format(int(Results[1]) - int(Results[10])))
        print("The total number of trades simulated: {0}".format(int(Results[10])))
        print("The total amount of spreads traded is: {0}".format(int(Results[2])))
        print("The number of trades fully won is: {0}".format(int(Results[3])))
        print("The number of trades partially won is: {0}".format(int(Results[4])))
        print("The number of trades partially lost is: {0}".format(int(Results[5])))
        print("The number of trades fully lost is: {0}".format(int(Results[6])))
        print("The total amount spent on taxes is: ${0}".format(round(float(Results[7]),2)))
        print("The total amount spent in comissions is: ${0}".format(round(float(Results[8]), 2)))
        print("\n")
