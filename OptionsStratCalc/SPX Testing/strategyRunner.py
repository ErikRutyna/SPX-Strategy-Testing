import os
import numpy as np
import datetime 
import backtesting_strats_spx as BTSPX
import csv

Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\BacktestResults"

# Initial Financial Info
InitialBalance =  3000
MaxRiskTrade = 500/3000
Delta = [0.15, 0.20, 0.25, 0.3, 0.35, 0.4]
Scaling = ["width","contracts"]
MaxRiskTotal = 20000

# start date - must start in/after Jan 6 '17 for MWF sPY options due to limite ddata
# Good dates to test are on (YEAR-MONTH-DAY):
# 2020 - 1 - 2
# 2016 - 1 - 5
# 2017 - 1 - 6
StartDate = datetime.datetime(2016, 1, 5)


for i in range(len(Delta)):
     for j in range(len(Scaling)):

          Conditions = np.array([InitialBalance, MaxRiskTrade, Delta[i], MaxRiskTotal])
          Results, Balance = BTSPX.PCS_SPX(Conditions, StartDate, Scaling[j])

          # save the PCs stuff to 2 files, one for results, one for account balances
          PCSRName = "PCS-{0}delta-{1}-scaling.txt".format(Delta[i], Scaling[j])
          PCSBname = "PCS-{0}delta-{1}-scaling-balances.csv".format(Delta[i], Scaling[j])
          PCSRFile = os.path.join(Folder, PCSRName)
          PCSBFile = os.path.join(Folder, PCSBname)

          S1 = "The final profit with delta = {0} and scaling via ".format(Delta[i])\
               + Scaling[j] + " is =: ${0}\n".format(round(float(Results[0]),2))
          S2 ="The average return on collateral per trade is: {0}%\n".format(round(float(Results[9]),4))
          S3 ="The total number of trades = done: {0}\n".format(int(Results[1]))
          S4 ="The total number of historical trades is: {0}\n".format(int(Results[1]) - int(Results[10]))
          S5 ="The total number of trades simulated: {0}\n".format(int(Results[10]))
          S6 ="The total amount of spreads traded is: {0}\n".format(int(Results[2]))
          S7 ="The number of trades fully won is: {0}\n".format(int(Results[3]))
          S8 ="The number of trades partially won is: {0}\n".format(int(Results[4]))
          S9 ="The number of trades partially lost is: {0}\n".format(int(Results[5]))
          S10 ="The number of trades fully lost is: {0}\n".format(int(Results[6]))
          S11="The total amount spent on taxes is: ${0}\n".format(round(float(Results[7]),2))
          S12 = "The total amount spent in comissions is: ${0}\n".format(round(float(Results[8]), 2))

          with open(PCSRFile, "w") as PCRFile:
               PCRFile.write(S1)
               PCRFile.write(S2)
               PCRFile.write(S3)
               PCRFile.write(S4)
               PCRFile.write(S5)
               PCRFile.write(S6)
               PCRFile.write(S7)
               PCRFile.write(S8)
               PCRFile.write(S9)
               PCRFile.write(S10)
               PCRFile.write(S11)
               PCRFile.write(S12)

          with open(PCSBFile, "w", newline="") as PCSBFile:
               fieldnames = ["bal", "date"]
               writer = csv.writer(PCSBFile)
               writer.writerow(fieldnames)
               for q in range(len(Balance[0])):
                    writer.writerow([str(round(Balance[0][q],2)), Balance[1][q]])


          Conditions = np.array([InitialBalance, MaxRiskTrade, Delta[i], MaxRiskTotal])
          Results, Balance = BTSPX.CCS_SPX(Conditions, StartDate, Scaling[j])

          # save the PCs stuff to 2 files, one for results, one for account balances
          PCSRName = "CCS-{0}delta-{1}-scaling.txt".format(Delta[i], Scaling[j])
          PCSBname = "CCS-{0}delta-{1}-scaling-balances.csv".format(Delta[i], Scaling[j])
          PCSRFile = os.path.join(Folder, PCSRName)
          PCSBFile = os.path.join(Folder, PCSBname)

          S1 = "The final profit with delta = {0} and scaling via ".format(Delta[i])\
               + Scaling[j] + " is =: ${0}\n".format(round(float(Results[0]),2))
          S2 ="The average return on collateral per trade is: {0}%\n".format(round(float(Results[9]),4))
          S3 ="The total number of trades = done: {0}\n".format(int(Results[1]))
          S4 ="The total number of historical trades is: {0}\n".format(int(Results[1]) - int(Results[10]))
          S5 ="The total number of trades simulated: {0}\n".format(int(Results[10]))
          S6 ="The total amount of spreads traded is: {0}\n".format(int(Results[2]))
          S7 ="The number of trades fully won is: {0}\n".format(int(Results[3]))
          S8 ="The number of trades partially won is: {0}\n".format(int(Results[4]))
          S9 ="The number of trades partially lost is: {0}\n".format(int(Results[5]))
          S10 ="The number of trades fully lost is: {0}\n".format(int(Results[6]))
          S11="The total amount spent on taxes is: ${0}\n".format(round(float(Results[7]),2))
          S12 = "The total amount spent in comissions is: ${0}\n".format(round(float(Results[8]), 2))

          with open(PCSRFile, "w") as PCRFile:
               PCRFile.write(S1)
               PCRFile.write(S2)
               PCRFile.write(S3)
               PCRFile.write(S4)
               PCRFile.write(S5)
               PCRFile.write(S6)
               PCRFile.write(S7)
               PCRFile.write(S8)
               PCRFile.write(S9)
               PCRFile.write(S10)
               PCRFile.write(S11)
               PCRFile.write(S12)

          with open(PCSBFile, "w", newline="") as PCSBFile:
               fieldnames = ["bal", "date"]
               writer = csv.writer(PCSBFile)
               writer.writerow(fieldnames)
               for q in range(len(Balance[0])):
                    writer.writerow([str(round(Balance[0][q],2)), Balance[1][q]])



          Conditions = np.array([InitialBalance, MaxRiskTrade, Delta[i], MaxRiskTotal])
          Results, Balance = BTSPX.ICS_SPX(Conditions, StartDate, Scaling[j])

          # save the PCs stuff to 2 files, one for results, one for account balances
          PCSRName = "ICS-{0}delta-{1}-scaling.txt".format(Delta[i], Scaling[j])
          PCSBname = "ICS-{0}delta-{1}-scaling-balances.csv".format(Delta[i], Scaling[j])
          PCSRFile = os.path.join(Folder, PCSRName)
          PCSBFile = os.path.join(Folder, PCSBname)

          S1 = "The final profit with delta = {0} and scaling via ".format(Delta[i])\
               + Scaling[j] + " is =: ${0}\n".format(round(float(Results[0]),2))
          S2 ="The average return on collateral per trade is: {0}%\n".format(round(float(Results[9]),4))
          S3 ="The total number of trades = done: {0}\n".format(int(Results[1]))
          S4 ="The total number of historical trades is: {0}\n".format(int(Results[1]) - int(Results[10]))
          S5 ="The total number of trades simulated: {0}\n".format(int(Results[10]))
          S6 ="The total amount of spreads traded is: {0}\n".format(int(Results[2]))
          S7 ="The number of trades fully won is: {0}\n".format(int(Results[3]))
          S8 ="The number of trades partially won is: {0}\n".format(int(Results[4]))
          S9 ="The number of trades partially lost is: {0}\n".format(int(Results[5]))
          S10 ="The number of trades fully lost is: {0}\n".format(int(Results[6]))
          S11="The total amount spent on taxes is: ${0}\n".format(round(float(Results[7]),2))
          S12 = "The total amount spent in comissions is: ${0}\n".format(round(float(Results[8]), 2))

          with open(PCSRFile, "w") as PCRFile:
               PCRFile.write(S1)
               PCRFile.write(S2)
               PCRFile.write(S3)
               PCRFile.write(S4)
               PCRFile.write(S5)
               PCRFile.write(S6)
               PCRFile.write(S7)
               PCRFile.write(S8)
               PCRFile.write(S9)
               PCRFile.write(S10)
               PCRFile.write(S11)
               PCRFile.write(S12)

          with open(PCSBFile, "w", newline="") as PCSBFile:
               fieldnames = ["bal", "date"]
               writer = csv.writer(PCSBFile)
               writer.writerow(fieldnames)
               for q in range(len(Balance[0])):
                    writer.writerow([str(round(Balance[0][q],2)), Balance[1][q]])
