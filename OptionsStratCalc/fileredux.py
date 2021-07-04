import csv
import os

Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"

SPXPutChain = "SPXPutsChainRev.csv"
SPXCallsChain = "SPXCallsChain.csv"

SPXCallsChain = os.path.join(Folder, SPXCallsChain)
SPXPutChain = os.path.join(Folder, SPXPutChain)
SPXCallPath = os.path.join(Folder, "Calls2.csv")
SPXPutPath = os.path.join(Folder, "Puts.csv")

with open(SPXCallsChain) as DataFile:
    SPXCallsChain = list(csv.reader(DataFile))
SPXCallsChain.reverse()

print(len(SPXCallsChain))

for i in range(len(SPXCallsChain), -1, -1):
    if i == 1: break
    Delta = abs(float(SPXCallsChain[i-1][7]))
    if (Delta) > 0.5 or (Delta) < 0.01:
        del SPXCallsChain[i-1]


print(len(SPXCallsChain))

with open(SPXCallPath, 'w', newline='') as file:
    writer = csv.writer(file)
    for line in SPXCallsChain:
        writer.writerow(line)



print("done")