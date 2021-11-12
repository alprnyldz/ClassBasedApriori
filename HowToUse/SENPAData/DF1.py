from CLASSBASEDAPRIORI import ClassBasedAprioriLibrary
from datetime import datetime
import pandas as pd
import numpy as np, scipy.stats as st
import statistics
import time



df = pd.read_csv("/Users/alpereny/Eliar/DATABASE/SENPA mekatronik/jobarchive.csv", sep="\\t", lineterminator="\r", engine='python')

df = df.replace({'MACHTEXT': {'1-(450-1) KROMSAN': 'Kromsan450-1',
                              '2-(600-1) KROMSAN': 'Kromsan600-1',
                              '3-(150-1) KROMSAN': 'Kromsan150-1',
                              '4-(300-1) KROMSAN': 'Kromsan300-1',
                              '5-(50-1) KROMSAN': 'Kromsan50-1',
                              '06-(1400-1) YEN.CANLAR': 'YenCanlar1400-1',
                              '07-(600-2) YEN.CANLAR': 'YenCanlar600-2',
                              '8-(1500-1) E.CANLAR': 'ECanlar1500-1',
                              '9-(1500-2) E.CANLAR': 'ECanlar1500-2',
                              '10-(50-2)Y.CANLAR': 'YCanlar50-2',
                              '11-(50-3) Y.CANLAR': 'YCanlar50-3',
                              '12-(50-4)Y.CANLAR': 'YCanlar50-4',
                              '13-(50-5) Y.CANLAR': 'YCanlar50-5',
                              '14-(100-1) Y.CANLAR -1': 'YCanlar100-1',
                              '15-(100-2) Y.CANLAR': 'YCanlar100-2',
                              '16-(200-1) Y.CANLAR -1': 'YCanlar200-1',
                              '17-(200-2) Y.CANLAR': 'YCanlar200-2',
                              '18-(300-2) Y.CANLAR-1': 'YCanlar300-2',
                              '19-(100-3) y.canlar': 'YCanlar100-3',
                              '20-(400-1)YEN.CANLAR': 'YenCanlar400-2',
                              '21-(900-1) E.CANLAR': 'ECanlar900-1',
                              '22-(900-2) E.CANLAR': 'ECanlar900-2',
                              '23-(150-2) y.canlar': 'YCanlar150-2',
                              'BRUGNER RAM -1': 'BrugnerRam',
                              'RAM  HAS GRUP': 'RamHasGrup',
                              'SANTEX KURUTMA': 'SantexKurutma',
                              'RAM MONFORST': 'RamMonforst'}
                 })


df['SAPMA'] = None
for index in df.index:
    try:
        df.at[index, 'SAPMA'] = (float(df.at[index, 'WEIGHTEDVALUE']) - df.at[index, 'TARGETVALUE']) / df.at[index, 'TARGETVALUE']
    except:
        continue

sapmaList = df.SAPMA.dropna().to_list()
cI = st.t.interval(0.99, len(sapmaList)-1, loc=0, scale=st.sem(sapmaList))
quantiles = statistics.quantiles(sapmaList, n=10)
ci3 = (-0.25, 0.10)
df['CI'] = None
for index in df.index:
    if df.at[index,'SAPMA'] == None:
        continue
    if quantiles[0] < df.at[index, 'SAPMA'] < quantiles[-1]:
        df.at[index, 'CI'] = 'True'
    else:
        df.at[index, 'CI'] = 'False'

df = df.sort_values(by=['REQUESTTIME', 'WEIGHNO'])
df = df.reset_index(drop=True)

df = df.drop(columns=
             ['JOBARCHIVEKEYFIELD', 'JOBDATE', 'JOBNO', 'STATUS', 'MACHINENO', 'RECSTEPNO',
              'LINENO', 'IKIZMAKNO', 'LANGNUMBER', 'TARGETWATER', 'IKIZMACHTEXT', 'JOBNOWEIGHNOTEXT',
              'WEIGHTEDVALUEVOLUME', 'WEIGHTEDWATERVOLUME', 'BATCHBEKLEMEDE', 'LOTCODE', 'ACHEMCODE', 'P2', 'P3',
              'TANKNO', 'DB_KEY'])


columnNames = ['REQUESTTIME', 'TOTALJOBNO', 'WEIGHNO', 'STARTINGTIME', 'ENDTIME', "TIMETAKEN", 'DURATION', 'CHEMICALNO', 'CHEMTEXT', 'MACHTEXT',
               'STATUSTEXT', 'TARGETVALUE', 'WEIGHTEDVALUE', 'WEIGHTEDWATER', 'PRIORITY', 'REQUESTER',  'P1', 'PRGNO',
               'PRGSTEPNO', 'CORRECTION', 'ADDITION', 'BATCHCODE', 'DSTNO', 'HEDEFSAHATANKNO']

df = df[['TOTALJOBNO', 'CHEMICALNO', 'CHEMTEXT', 'MACHTEXT', 'STATUSTEXT', 'CI']]

df = df.astype(str)
length = len(df)

rowIndex = 0
while rowIndex < length-1:
    df.at[rowIndex, 'CHEMICALNO'] = [df.at[rowIndex, 'CHEMICALNO']]
    df.at[rowIndex, 'CHEMTEXT'] = [df.at[rowIndex, 'CHEMTEXT']]
    df.at[rowIndex, 'MACHTEXT'] = [df.at[rowIndex, 'MACHTEXT']]
    df.at[rowIndex, 'STATUSTEXT'] = [df.at[rowIndex, 'STATUSTEXT']]
    df.at[rowIndex, 'CI'] = [df.at[rowIndex, 'CI']]
    i = 1
    while df.at[rowIndex, 'TOTALJOBNO'] == df.at[rowIndex+i, 'TOTALJOBNO']:
        df.at[rowIndex, 'CHEMICALNO'].append(df.at[rowIndex+i, 'CHEMICALNO'])
        df.at[rowIndex, 'CHEMTEXT'].append(df.at[rowIndex+i, 'CHEMTEXT'])
        df = df.drop(rowIndex+i, axis=0)
        i += 1
    rowIndex += i

del rowIndex, length, i, cI, columnNames, quantiles, ci3, index

df = df.drop(columns=['TOTALJOBNO'])
df = df.reset_index(drop=True)
df2 = df[['CHEMICALNO', 'MACHTEXT', 'STATUSTEXT', 'CI']]
df2 = df2.drop(64169, axis=0)

start = time.time()
classBasedApriori_SENPA = ClassBasedAprioriLibrary.ClassBasedApriori(df2, supportThreshold=0.001)
end = time.time()
print(end - start)
del start, end


assoc = classBasedApriori_SENPA.CreateAssociationsToAnalyze(associatedClassNames=["STATUSTEXT"],
                                    condAssociatedItem='STATUSTEXT: IPTAL EDILDI')
classBasedApriori_SENPA.Plot(assoc)

assoc2 =classBasedApriori_SENPA.CreateAssociationsToAnalyze(associatedClassNames=["CI"],
                                    condAssociatedItem='CI: False')
classBasedApriori_SENPA.Plot(assoc2)

supportList = [x.support for x in assoc2]
confidenceList = [x.confidence for x in assoc2]
liftList = [x.lift for x in assoc2]
assoc2_1 = [association for association in assoc2
                                         if
                                         (
                                             association.confidence >= 0.75
                                             and
                                             association.lift >= statistics.median(liftList)
                                         )
                                         ]
classBasedApriori_SENPA.Plot(assoc2_1)


assoc3 = classBasedApriori_SENPA.CreateAssociationsToAnalyze(baseClassNames=["MACHTEXT"], associatedClassNames=["CHEMICALNO"], fragmentation='unfragmentedAssociations')
classBasedApriori_SENPA.Plot(assoc3)

assoc4 = classBasedApriori_SENPA.CreateAssociationsToAnalyze(baseClassNames=["CHEMICALNO"], associatedClassNames=["CHEMICALNO"], fragmentation='innerAssociations')
classBasedApriori_SENPA.Plot(assoc4)


start = time.time()
classBasedApriori_SENPA = ClassBasedAprioriLibrary.ClassBasedApriori(df, supportThreshold=0.0001)
end = time.time()
print(end - start)
del start, end
