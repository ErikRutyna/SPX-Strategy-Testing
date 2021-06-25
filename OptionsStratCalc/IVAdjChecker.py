import optionsCalc as OC
import spy_price_adjuster as PA
from yahoo_fin import stock_info as si
import tickerCleanup_WBS as tbw

tbw.miscCallsCleaner()

IVAdjFits = PA.spy_price_adjust()

Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData"
SPYData = "spy_testing_data"
SPYPrices = "spy_historical_data"
VIXPrices = "vix_historical_data"
SPYCalls = "spy_calls_data"
IVFitsP = OC.impv_rel(Folder, SPYData, SPYPrices, VIXPrices, 8)


Name = "SPY"
Strike = 421
DTE = 2
Price =  si.get_live_price(Name)
RFRR = si.get_live_price("^TNX")
IV = si.get_live_price("^VIX")
IV = IVFitsP[DTE-1].slope * IV + IVFitsP[DTE-1].intercept


TestPut = OC.black_scholes(Name, Price, Strike, RFRR/100, DTE, IV/100, "P")
print("Test put has price of: ${0}".format(TestPut.price))

TestPutAdj = IVAdjFits[DTE-1].slope * (Strike - Price) + IVAdjFits[DTE-1].intercept
TestPutAdj = round(TestPut.price + TestPutAdj, 2)
print("Adjusted test put has price of: ${0}".format(TestPutAdj))