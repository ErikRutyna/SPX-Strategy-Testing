from typing import Optional
import optionsCalc as OC

F = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
OPT = "spy_testingDATA"
EOD = "spy_historical_data"
VIX = "vix_data_master"

Fits = OC.impv_rel(F, OPT, EOD, VIX, 8)
for i in range(len(Fits)):
    print(Fits[i])
    print("\n")
