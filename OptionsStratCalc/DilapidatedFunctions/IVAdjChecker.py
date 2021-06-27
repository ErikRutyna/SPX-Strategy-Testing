import optionsCalc as OC
from yahoo_fin import stock_info as si
import math


Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
SPYData = "spy_testing_data"
SPYPrices = "spy_historical_data"
VIXPrices = "vix_historical_data"
SPYCalls = "spy_calls_data"
IVFitsP = OC.impv_rel(Folder, SPYData, SPYPrices, VIXPrices, 8)


Name = "^SPX"

DTE = 5
Price =  si.get_live_price(Name)
Strike = 4285
RFRR = si.get_live_price("^TNX")
IV = si.get_live_price("^VIX")
# IV = IVFitsP[DTE-1].slope * IV + IVFitsP[DTE-1].intercept


TestPut = OC.black_scholes(Name, Price, Strike, RFRR/100, DTE, 7.47/100, "P")
TestCall = OC.black_scholes(Name, Price, Strike, RFRR/100, DTE, 7.47/100, "C")
TestCall2 = OC.black_scholes(Name, Price, Strike+1, RFRR/100, DTE, 7.33/100, "C")
print("Test put has price of: ${0}".format(TestPut.price))

# TestPutAdj = IVAdjFits[DTE-1].slope * (Strike - Price) + IVAdjFits[DTE-1].intercept
# TestPutAdj = round(TestPut.price + TestPutAdj, 2)
# print("Adjusted test put has price of: ${0}".format(TestPutAdj))