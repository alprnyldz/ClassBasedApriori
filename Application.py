import ClassBasedApriori as ClassBasedAprioriLibrary
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import time

baDataDF = pd.read_csv('BADATA.csv', sep=';')

start = time.time()

classBasedApriori_DF1_001 = ClassBasedAprioriLibrary.ClassBasedApriori(DF1)
end = time.time()
print(end - start)
del start, end

# if supportThreshhold == 0.001 -> 6.804093837738037 seconds

start = time.time()
classBasedApriori_DF1_000 = ClassBasedAprioriLibrary.ClassBasedApriori(DF1, supportThreshold=0)
end = time.time()
print(end - start)

# if supportThreshhold == 0.000 -> 53.30642127990723 seconds
# MacBook Pro (13-inch, 2019, Four Thunderbolt 3 ports)
# Processor 2,4 GHz Quad-Core Intel Core i5
# Memory 8 GB 2133 MHz LPDDR3

# +++++++++++++++++++++++++++++++++++++++++++++++ What is the probability that a PROGRAMNOLIST will be used when any MACHINECODE is seen?

assoc = classBasedApriori_DF1_001.CreateAssociationsToAnalyze(baseClassNames=["MACHINECODE"], associatedClassNames=["PROGRAMNOLIST"],
                                                              condAssociatedItem='PROGRAMNOLIST: 1000')
assocc = classBasedApriori_DF1_001.CreateAssociationsToAnalyze(baseClassNames=["MACHINECODE"], associatedClassNames=["PROGRAMNOLIST"],
                                                               condAssociatedItem='PROGRAMNOLIST: 800')

supportList = [x.support for x in assoc]
supportList.sort(key=lambda x: x, reverse=True)
confidenceList = [x.confidence for x in assoc]
liftList = [x.lift for x in assoc]
plt.hist(supportList, bins=10)
plt.hist(confidenceList)
plt.hist(liftList)

classBasedApriori_DF1_001.Plot(assoc)
assoc.sort(key=lambda x: x.confidence, reverse=True)
classBasedApriori_DF1_001.Print(assoc)
classBasedApriori_DF1_001.Plot(assoc)

# ----------------------------------------------- What is the probability that a PROGRAMNOLIST will be used when any MACHINECODE is seen?


# +++++++++++++++++++++++++++++++++++++++++++++++ What is the probability that a PROGRAMNOLIST will be used on any MACHINECODE?

assoc = classBasedApriori_DF1_001.CreateAssociationsToAnalyze(baseClassNames=["PROGRAMNOLIST"], associatedClassNames=["MACHINECODE"],
                                                              condBaseItem='PROGRAMNOLIST: 1010')
assocc = classBasedApriori_DF1_001.CreateAssociationsToAnalyze(baseClassNames=["PROGRAMNOLIST"], associatedClassNames=["MACHINECODE"],
                                                               condBaseItem='PROGRAMNOLIST: 800')

supportList = [x.support for x in assoc]
confidenceList = [x.confidence for x in assoc]
liftList = [x.lift for x in assoc]
plt.hist(supportList, bins=100)
plt.hist(confidenceList)
plt.hist(liftList)

classBasedApriori_DF1_001.Plot(assoc)
assoc.sort(key=lambda x: x.confidence, reverse=True)
classBasedApriori_DF1_001.Print(assoc)

supportList = [x.support for x in assocc]
confidenceList = [x.confidence for x in assocc]
liftList = [x.lift for x in assocc]
plt.hist(supportList, bins=100)
plt.hist(confidenceList)
plt.hist(liftList)

classBasedApriori_DF1_001.Plot(assocc)
assocc.sort(key=lambda x: x.confidence, reverse=True)
classBasedApriori_DF1_001.Print(assocc)

# ----------------------------------------------- What is the probability that a PROGRAMNOLIST will be used on any MACHINECODE?


# +++++++++++++++++++++++++++++++++++++++++++++++ Which PROGRAMNOLISTs did any MACHINECODE use?

assoc2 = classBasedApriori_DF1_000.CreateAssociationsToAnalyze(baseClassNames=["MACHINECODE"], associatedClassNames=["PROGRAMNOLIST"],
                                                               condBaseItem='MACHINECODE: 20-300', fragmentation='unfragmentedAssociations')

supportList = [x.support for x in assoc2]
supportList.sort(key=lambda x: x, reverse=True)
confidenceList = [x.confidence for x in assoc2]
liftList = [x.lift for x in assoc2]
plt.hist(supportList)
plt.hist(confidenceList)
plt.hist(liftList)

classBasedApriori_DF1_001.Plot(assoc2)

# ----------------------------------------------- Which PROGRAMNOLISTs did any MACHINECODE use?


# +++++++++++++++++++++++++++++++++++++++++++++++ from machines to programnolist unfragmentedassociations

assoc5 = classBasedApriori_DF1_001.CreateAssociationsToAnalyze \
    (baseClassNames=["MACHINECODE"], associatedClassNames=["PROGRAMNOLIST"], fragmentation='unfragmentedAssociations')

assoc5.sort(key=lambda x: x.confidence, reverse=True)

dictt = {}
for association in assoc5:
    try:
        dictt[str(frozenset(association.baseItems))[11:-2]].append(association)
    except KeyError:
        dictt[str(frozenset(association.baseItems))[11:-2]] = [association]

for i in range(0, len(dictt)):
    classBasedApriori_DF1_001.Plot(list(dictt.values())[i])

for machineName, associations in dictt.items():
    sum = 0
    for association in associations:
        sum += association.confidence
    print(machineName, sum)

supportList = [x.support for x in assoc5]
confidenceList = [x.confidence for x in assoc5]
liftList = [x.lift for x in assoc5]
assoc5_1 = [association for association in assoc5
            if
            (
                    association.support >= supportList[int(len(supportList) / 100 * 5)]
                    and
                    association.confidence >= statistics.median(confidenceList)
                    and
                    association.lift >= statistics.median(liftList)
            )
            ]
dictt = {}
for association in assoc5_1:
    try:
        dictt[str(frozenset(association.baseItems))[11:-2]].append(association)
    except KeyError:
        dictt[str(frozenset(association.baseItems))[11:-2]] = [association]
for i in range(0, len(dictt)):
    classBasedApriori_DF1_001.Plot(list(dictt.values())[i])

classBasedApriori_DF1_001.PlotInteractive(assoc5, fileDirectory='bar_chart.svg')

# ----------------------------------------------- from machines to programnolist unfragmentedassociations


# +++++++++++++++++++++++++++++++++++++++++++++++ from machines to programnolist fragmentedassociations

assoc7 = classBasedApriori_DF1_001.CreateAssociationsToAnalyze \
    (baseClassNames=["MACHINECODE"], associatedClassNames=["PROGRAMNOLIST"])

assoc7.sort(key=lambda x: x.confidence, reverse=True)

dictt = {}
for association in assoc7:
    try:
        dictt[str(frozenset(association.baseItems))[11:-2]].append(association)
    except KeyError:
        dictt[str(frozenset(association.baseItems))[11:-2]] = [association]

for i in range(0, len(dictt)):
    classBasedApriori_DF1_001.Plot(list(dictt.values())[i])

for machineName, associations in dictt.items():
    sum = 0
    for association in associations:
        sum += association.confidence
    print(machineName, sum)

supportList = [x.support for x in assoc7]
confidenceList = [x.confidence for x in assoc7]
liftList = [x.lift for x in assoc7]
assoc7_1 = [association for association in assoc7
            if
            (
                    association.support >= supportList[int(len(supportList) / 100 * 5)]
                    and
                    association.confidence >= statistics.median(confidenceList)
                    and
                    association.lift >= statistics.median(liftList)
            )
            ]
dictt = {}
for association in assoc7_1:
    try:
        dictt[str(frozenset(association.baseItems))[11:-2]].append(association)
    except KeyError:
        dictt[str(frozenset(association.baseItems))[11:-2]] = [association]
for i in range(0, len(dictt)):
    classBasedApriori_DF1_001.Plot(list(dictt.values())[i])

# ----------------------------------------------- from machines to programnolist fragmentedassociations
