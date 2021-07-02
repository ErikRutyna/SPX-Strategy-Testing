import csv
import datetime
import os
import numpy as np

Folder = r"C:\Users\Erik\Desktop\devMisc\OptionsCalc\MasterData\SPY and SPX Options Data"

SPXPutChain = "SPXPutsChainRev.csv"
SPXCallsChain = "SPXCallsChain.csv"

SPXCallsChain = os.path.join(Folder, SPXCallsChain)
SPXPutChain = os.path.join(Folder, SPXPutChain)
SPXCallPath = os.path.join(Folder, "Calls.csv")
SPXPutPath = os.path.join(Folder, "Puts.csv")

with open(SPXPutChain) as DataFile:
    SPXPutChain = list(csv.reader(DataFile))

with open(SPXCallsChain) as DataFile:
    SPXCallsChain = list(csv.reader(DataFile))
SPXCallsChain.reverse()

print(len(SPXCallsChain))
print(len(SPXPutChain))

for i in range(len(SPXCallsChain), -1, -1):
    if i == 1: break
    Delta = abs(float(SPXCallsChain[i-1][7]))
    if (Delta) > 0.5 or (Delta) < 0.05:
        del SPXCallsChain[i-1]

for i in range(len(SPXPutChain), -1, -1):
    if i == 1: break
    Delta = abs(float(SPXPutChain[i-1][7]))
    if (Delta) > 0.5 or (Delta) < 0.05:
        del SPXPutChain[i-1]

print(len(SPXCallsChain))
print(len(SPXPutChain))

with open(SPXCallPath, 'w', newline='') as file:
    writer = csv.writer(file)
    for line in SPXCallsChain:
        writer.writerow(line)

with open(SPXPutPath, 'w', newline='') as file:
    writer = csv.writer(file)
    for line in SPXPutChain:
        writer.writerow(line)

print("done")