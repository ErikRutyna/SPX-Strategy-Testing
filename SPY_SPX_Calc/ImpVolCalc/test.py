from typing import Optional
import ImpliedVolatilityRelator as IVR

F = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
OPT = "spy_testingDATA"
EOD = "spy_historical_data"
VIX = "vix_data_master"
Sty = "A"

IVR.vix_correlator(F, OPT, EOD, VIX, Sty)