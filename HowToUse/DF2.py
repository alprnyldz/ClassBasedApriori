from CLASSBASEDAPRIORI import ClassBasedAprioriLibrary
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import time

baDataDF = pd.read_csv('/Users/alpereny/Eliar/DATABASE/BADATA.csv', sep=';')


DF2 = baDataDF[["MACHINECODE", "PROGRAMNOLIST"]].copy()
DF2["DUMMYSTATUS"] = None
for i in range(len(baDataDF)):
    DF2.at[i, "PROGRAMNOLIST"] = DF2.at[i, "PROGRAMNOLIST"].split(',')
    if DF2.at[i, "MACHINECODE"] == '19-100' or '800' in DF2.at[i, "PROGRAMNOLIST"]:  # better for fragmented
        DF2.at[i, "DUMMYSTATUS"] = '1'
    else:
        DF2.at[i, "DUMMYSTATUS"] = '0'
    DF2.at[i, "DUMMYSTATUS"] = [DF2.at[i, "DUMMYSTATUS"]]
    DF2.at[i, "MACHINECODE"] = [DF2.at[i, "MACHINECODE"]]
del i


start = time.time()
classBasedAppriori_DF2_001 = ClassBasedAprioriLibrary.ClassBasedApriori(DF2)
end = time.time()
print(end - start)
del start, end

# if supportThreshhold == 0.001 -> 31.46102809906006, 59.71157789230347, 37.57880187034607, 36.87619209289551


start = time.time()
classBasedAppriori_DF2_000 = ClassBasedAprioriLibrary.ClassBasedApriori(DF2, supportThreshold=0)
end = time.time()
print(end - start)

# if supportThreshhold == 0.000 -> 266.0478160381317, 291.128751039505, 388.9250109195709


assoc6 = classBasedAppriori_DF2_001.CreateAssociationsToAnalyze(associatedClassNames=["DUMMYSTATUS"],
                                    condAssociatedItem='DUMMYSTATUS: 1')
supportList = [x.support for x in assoc6]
supportList.sort(key=lambda x: x, reverse=True)
confidenceList = [x.confidence for x in assoc6]
liftList = [x.lift for x in assoc6]
plt.hist(supportList, bins=100, label='Histogram of Support')
plt.hist(confidenceList, bins=100)
plt.hist(liftList, bins=100)


classBasedAppriori_DF2_001.Plot(assoc6)


assoc6_1 = [association for association in assoc6
                                         if
                                         (
                                             association.support >= supportList[int(len(supportList)/100*5)]
                                             and
                                             association.confidence >= statistics.median(confidenceList)
                                             and
                                             association.lift >= statistics.median(liftList)
                                         )
                                         ]

classBasedAppriori_DF2_001.Plot(assoc6_1)


# unfragmented:
assoc9 = classBasedAppriori_DF2_001.CreateAssociationsToAnalyze(associatedClassNames=["DUMMYSTATUS"],
                                    condAssociatedItem='DUMMYSTATUS: 1', fragmentation='unfragmentedAssociations')
supportList = [x.support for x in assoc9]
supportList.sort(key=lambda x: x, reverse=True)
confidenceList = [x.confidence for x in assoc9]
liftList = [x.lift for x in assoc9]
plt.hist(supportList, bins=100, label='Histogram of Support')
plt.hist(confidenceList, bins=100)
plt.hist(liftList, bins=100)

classBasedAppriori_DF2_001.Plot(assoc9)

assoc9_1 = [association for association in assoc9
                                         if
                                         (
                                             association.support >= supportList[int(len(supportList)/100*5)]
                                             and
                                             association.confidence >= statistics.median(confidenceList)
                                             and
                                             association.lift >= statistics.median(liftList)
                                         )
                                         ]

classBasedAppriori_DF2_001.Plot(assoc9_1)




