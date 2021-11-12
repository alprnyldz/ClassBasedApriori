from CLASSBASEDAPRIORI import ClassBasedAprioriLibrary
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import time

baDataDF = pd.read_csv('/Users/alpereny/Eliar/DATABASE/BADATA.csv', sep=';')


DF3 = baDataDF[["MACHINECODE", "PROGRAMNOLIST"]].copy()
DF3["DUMMYSTATUS"] = None
for i in range(len(baDataDF)):
    DF3.at[i, "PROGRAMNOLIST"] = DF3.at[i, "PROGRAMNOLIST"].split(',')
    if DF3.at[i, "MACHINECODE"] == '8-600' or ['491'] == DF3.at[i, "PROGRAMNOLIST"]:  # better for unfragmented
        DF3.at[i, "DUMMYSTATUS"] = '1'
    else:
        DF3.at[i, "DUMMYSTATUS"] = '0'
    DF3.at[i, "DUMMYSTATUS"] = [DF3.at[i, "DUMMYSTATUS"]]
    DF3.at[i, "MACHINECODE"] = [DF3.at[i, "MACHINECODE"]]
del i

start = time.time()
classBasedAppriori_DF3_001 = ClassBasedAprioriLibrary.ClassBasedApriori(DF3)
end = time.time()
print(end - start)

# if supportThreshhold == 0.001 -> 34.58063888549805, 36.905415296554565

start = time.time()
classBasedAppriori_DF3_000 = ClassBasedAprioriLibrary.ClassBasedApriori(DF3, supportThreshold=0)
end = time.time()
print(end - start)

# if supportThreshhold == 0.000 -> 376.9449369907379, 387.32928824424744



# DF3, fragmented
assoc3 = \
    classBasedAppriori_DF3_001.CreateAssociationsToAnalyze\
        (associatedClassNames=["DUMMYSTATUS"], condAssociatedItem='DUMMYSTATUS: 1',
         fragmentation='fragmentedAssociations')

assoc3.sort(key=lambda x: x.support, reverse=True)
classBasedAppriori_DF3_001.Plot(assoc3)

# DF3, unfragmented if supportThreshhold == 0.001, net çözüm
assoc4_001 = \
    classBasedAppriori_DF3_001.CreateAssociationsToAnalyze\
        (associatedClassNames=["DUMMYSTATUS"], condAssociatedItem='DUMMYSTATUS: 1',
         fragmentation="unfragmentedAssociations")

assoc4_001.sort(key=lambda x: x.support, reverse=True)
classBasedAppriori_DF3_001.Plot(assoc4_001)


# if supportThreshhold == 0.000
assoc4_000 = \
    classBasedAppriori_DF3_000.CreateAssociationsToAnalyze\
        (associatedClassNames=["DUMMYSTATUS"], condAssociatedItem='DUMMYSTATUS: 1',
         minConfidence=1, fragmentation="unfragmentedAssociations")

supportList = [x.support for x in assoc4_000]
assoc4_000 = [association for association in assoc4_000
                                         if
                                         (
                                             association.support >= supportList[int(len(supportList)/100*5)]
                                             and
                                             association.lift >= statistics.median([x.lift for x in assoc4_000])
                                         )
                                         ]
assoc4_000.sort(key=lambda x: x.support, reverse=True)
classBasedAppriori_DF3_001.Plot(assoc4_000)

