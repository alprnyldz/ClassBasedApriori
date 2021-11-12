from CLASSBASEDAPRIORI import ClassBasedAprioriLibrary
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import time

baDataDF = pd.read_csv('/Users/alpereny/Eliar/DATABASE/BADATA.csv', sep=';')

DF1 = baDataDF[["MACHINECODE", "PROGRAMNOLIST"]].copy()
for i in range(len(baDataDF)):
    DF1.at[i, "PROGRAMNOLIST"] = DF1.at[i, "PROGRAMNOLIST"].split(',')
    DF1.at[i, "MACHINECODE"] = [DF1.at[i, "MACHINECODE"]]
del i

classBasedApriori_DF1_001 = ClassBasedAprioriLibrary.ClassBasedApriori(DF1)
classBasedApriori_DF1_000 = ClassBasedAprioriLibrary.ClassBasedApriori(DF1, supportThreshold=0)

innerAssoc = classBasedApriori_DF1_001.CreateAssociationsToAnalyze(fragmentation='innerAssociations')
innerAssoc = classBasedApriori_DF1_000.CreateAssociationsToAnalyze(fragmentation='innerAssociations')

classBasedApriori_DF1_001.Plot(innerAssoc)

supportList = [x.support for x in innerAssoc]
confidenceList = [x.confidence for x in innerAssoc]
liftList = [x.lift for x in innerAssoc]
plt.hist(supportList, bins=100, label='Histogram of Support')
plt.hist(confidenceList, bins=100)
plt.hist(liftList, bins=100)

classBasedApriori_DF1_001.Plot(innerAssoc)

innerAssoc2 = [association for association in innerAssoc
                                         if
                                         (
                                             association.support >= supportList[int(len(supportList)/100*5)]
                                             and
                                             association.confidence >= 0.95
                                             and
                                             association.lift >= statistics.median(liftList)
                                         )
                                         ]

classBasedApriori_DF1_001.Plot(innerAssoc2)
innerAssoc.sort(key=lambda x: x.confidence, reverse=True)
classBasedApriori_DF1_001.Print(innerAssoc2)



print('done')

"""
associations = associationManager.fragmentedAssociations[frozenset(('MACHINECODE',))][frozenset(('PROGRAMNOLIST',))].copy()
associations.sort(key=lambda x: x.confidence, reverse=True)
associationsToAnalyze = [association for association in associations if association.baseItems == set(('MACHINECODE: 19-100',))]
associationsToAnalyze = [association for association in associations if association.associatedItems == set(('PROGRAMNOLIST: 127',))]
"""
