import pandas as pd
from itertools import combinations
import itertools
import matplotlib.pyplot as plt
import pygal
import statistics


def flatten(l): return [item for sublist in l for item in sublist]  # used for turning multiple lists to one list


uniqueNameSeperator = ": "


class DataSetManager:
    def __init__(self, dataSetIn):
        self.rawDataSet = dataSetIn
        self.listDataSet = []
        self.classBasedDataSet = []

        self.length = len(dataSetIn)
        self.classNames = list(dataSetIn.columns)
        self.fragmentableClasses = []
        self.subsetClasses = []
        for i in range(2, self.classNames.__len__() + 1):
            for comb in itertools.combinations(self.classNames, i):
                self.subsetClasses.append(comb)

        self.classInfo = {}
        self.indexDict = {}  # indexDict
        self.uniqueName_ClassDict = {}
        self.uniqueName_ItemDict = {}  # self.uniqueName_ClassDict = {}

        self.CreateClassInfo()
        self.CreateDataSetManager()

    class Transaction:  # new name: classBasedItemSet
        def __init__(self, classNamesIn):
            self.classNames = classNamesIn
            self.fragmentables = []
            self.unfragmentables = []
            self.transactionSet = set()
            self.uniqueNameDict = {}
            self.isFragmented = None
            for className in classNamesIn:
                self.__dict__[className] = []

        def UpdateItem(self, itemIn, uniqueNameIn, classNameIn):
            self.__dict__[classNameIn].append(itemIn)
            self.transactionSet.add(uniqueNameIn)

        def Finalize(self, fragmentableClassesIn):
            # Finalize iki yerde çağrılıyor, ikisinde de fragmentableClassesIn, self.classNames'in bir subset'i değil.
            for fragmentableClass in fragmentableClassesIn:
                try:
                    if len(self.__dict__[fragmentableClass]) > 1:
                        self.fragmentables.append(fragmentableClass)
                except:
                    continue
            self.unfragmentables = list(set(self.classNames) - set(self.fragmentables))
            for className in self.classNames:
                for item in self.__dict__[className]:
                    uniqueName = className + uniqueNameSeperator + item
                    try:
                        self.uniqueNameDict[className].append(uniqueName)
                    except KeyError:
                        self.uniqueNameDict[className] = [uniqueName]

    class ClassData:
        def __init__(self, uniqueItemNameIn, uniqueArrayIn):
            self.uniqueItemName = uniqueItemNameIn
            self.uniqueCount = len(uniqueArrayIn)
            self.uniqueList = uniqueArrayIn
            self.isSingle = True  # by default, will be set to False if multivariate

    def CreateClassInfo(
            self):  # buraya class'ın single olup olmadığı bilgisi de işlenebilir. single olmaması fragmentable demektir. ama fragmentable class olup olmadığı transaction için mi önemli
        for className in self.classNames:
            self.classInfo[className] = \
                self.ClassData(className, set(x for l in self.rawDataSet.loc[:, className] for x in l))
            for index in range(self.length):
                if len(self.rawDataSet.at[index, className]) > 1:
                    self.classInfo[className].isSingle = False
                    break
        for key, value in self.classInfo.items():  # fragmentableClass'ları belirlemek için  # bunu transaction class'ının içerisine yaz. her transaction oluşturulduğunda çalıştırılsın en son.
            if not value.isSingle:
                self.fragmentableClasses.append(key)

    def CreateDataSetManager(self):
        for index in range(self.length):
            transactionToAddToList = []  # self.listDataSet
            trs = self.Transaction(self.classNames)  # self.classBasedDataSet

            for className in self.classNames:
                """
                # if the class is multivariate, set isSingle to False # you need to check every single variable to see if the class is multivariate.
                if len() > 1:
                    self.classInfo[className].isSingle = False
                """

                for item in self.rawDataSet.at[index, className]:
                    # set an unique name for item
                    uniqueName = className + uniqueNameSeperator + str(item)
                    self.uniqueName_ItemDict[
                        uniqueName] = item  # self.uniqueName_ClassDict[uniqueName] = className # daha önce eklendiyse bu key,value check if values are not the same, print
                    self.uniqueName_ClassDict[uniqueName] = className

                    # update the ClassBasedTransaction # it is needed to insert the information
                    trs.UpdateItem(item, uniqueName, className)  #

                    # create indexDict
                    try:
                        self.indexDict[uniqueName].append(index)
                    except KeyError:
                        self.indexDict[uniqueName] = [index]

                    transactionToAddToList.append(uniqueName)  # for the self.listDataSet

            trs.Finalize(self.fragmentableClasses)
            trs.isFragmented = False
            self.listDataSet.append(transactionToAddToList)
            self.classBasedDataSet.append(trs)

    def GetIndexesOfItemSet(self, itemSetIn):
        sum_indexes = None
        for item in itemSetIn:
            indexes = self.indexDict[item]
            if indexes is None:
                # No support for any set that contains a not existing item.
                return 0.0

            if sum_indexes is None:
                # Assign the indexes on the first time.
                sum_indexes = indexes
            else:
                # Calculate the intersection on not the first time.
                sum_indexes = list(set(sum_indexes) & set(indexes))
        return sum_indexes

    def GetSupportOfItemSet(self, itemSetIn):
        try:
            return len(self.GetIndexesOfItemSet(itemSetIn)) / self.length
        except TypeError:
            return 0

    def GetFragmentedItemsets(self, classBasedItemSetIn):
        def sub_lists(listIn):
            # store all the sublists
            sublist = []
            # first loop
            for i in range(len(listIn) + 1):
                # second loop
                for j in range(i + 1, len(listIn) + 1):
                    # slice the subarray
                    sub = listIn[i:j]
                    sublist.append(sub)
            return sublist

        innerTransactions = []
        for fragmentableClass in classBasedItemSetIn.fragmentables:
            itemLists = sub_lists(classBasedItemSetIn.__dict__[fragmentableClass])
            for itemList in itemLists:
                if itemList.__len__() <= 1:
                    continue
                innerTransaction = self.Transaction([fragmentableClass])
                for item in itemList:
                    uniqueName = fragmentableClass + uniqueNameSeperator + str(item)
                    innerTransaction.UpdateItem(item, uniqueName, fragmentableClass)
                innerTransaction.Finalize([fragmentableClass])
                innerTransaction.isFragmented = True
                innerTransactions.append(innerTransaction)

        # fragmentable class'ları tekrar check etmeden itemsetleri çıkaran bir algoritma yazılmalı. transaction.UpdateSet ten kurtarılmalı
        fragmentedClassBasedItemSets = []
        for subsetClass in self.subsetClasses:
            trs = self.Transaction(subsetClass)
            for Class in subsetClass:
                for item in classBasedItemSetIn.__dict__[Class]:
                    uniqueName = Class + uniqueNameSeperator + str(item)
                    trs.UpdateItem(item, uniqueName, Class)
            # transaction creator diye bir araç lazım
            trs.Finalize(self.fragmentableClasses)

            args = []
            for fragmentableClass in trs.fragmentables:
                args.append(sub_lists(trs.__dict__[fragmentableClass]))
            if len(args) == 0:  # itertools.procuct boş listeden de combinasyon döndürüyor: boş tuple
                trs.isFragmented = False
                fragmentedClassBasedItemSets.append(trs)
                continue
            for comb in itertools.product(*args):
                fragmentedClassBasedItemSet = self.Transaction(subsetClass)
                for fragmentableClassIndex in range(len(trs.fragmentables)):
                    for item in comb[fragmentableClassIndex]:
                        uniqueName = trs.fragmentables[fragmentableClassIndex] + uniqueNameSeperator + str(item)
                        fragmentedClassBasedItemSet.UpdateItem(item, uniqueName,
                                                               trs.fragmentables[fragmentableClassIndex])
                for unfragmentableClass in trs.unfragmentables:
                    for item in trs.__dict__[unfragmentableClass]:
                        uniqueName = unfragmentableClass + uniqueNameSeperator + str(item)
                        fragmentedClassBasedItemSet.UpdateItem(item, uniqueName, unfragmentableClass)
                fragmentedClassBasedItemSet.Finalize(trs.fragmentables)
                if set(fragmentedClassBasedItemSet.transactionSet) == set(trs.transactionSet):
                    fragmentedClassBasedItemSet.isFragmented = False
                else:
                    fragmentedClassBasedItemSet.isFragmented = True
                fragmentedClassBasedItemSets.append(fragmentedClassBasedItemSet)
        return fragmentedClassBasedItemSets, innerTransactions


class ItemSetTree:
    def __init__(self):
        self.tree = {}

    def UpdateItemSetTree(self, classBasedItemSetIn, indexIn):
        try:
            self.tree[frozenset(classBasedItemSetIn.transactionSet)].UpdateItemSet(indexIn)
        except KeyError:
            self.tree[frozenset(classBasedItemSetIn.transactionSet)] = ItemSet(classBasedItemSetIn, indexIn)


class ItemSet:
    def __init__(self, classBasedItemSetIn, indexIn):
        self.indexes = {}
        self.classBasedItemSet = classBasedItemSetIn
        self.count = 0
        self.associations = {}
        self.UpdateItemSet(indexIn)

    def UpdateItemSet(self, indexIn):
        self.indexes[indexIn] = True
        self.count += 1

    def GetIndexes(self):
        return list(self.indexes.keys())

    def AddAssociation(self, key, association):
        self.associations[key] = association


class Association:
    def __init__(self, baseClassNamesIn, associatedClassNamesIn, supportIn, countIn, confidenceIn, liftIn,
                 baseItemsSetIn, associatedItemsSetIn):
        self.baseClassNames = baseClassNamesIn
        self.associatedClassNames = associatedClassNamesIn
        self.support = supportIn
        self.count = countIn
        self.confidence = confidenceIn
        self.lift = liftIn
        self.baseItems = baseItemsSetIn
        self.associatedItems = associatedItemsSetIn
        self.items = baseItemsSetIn.union(associatedItemsSetIn)


class AssociationManager:
    def __init__(self, classNamesIn, fragmentableClassesIn):
        self.unfragmentedAssociations = {}
        self.fragmentedAssociations = {}
        self.innerAssociations = {}

        for base_length in range(1, len(classNamesIn)):
            for baseClassNames in combinations(classNamesIn, base_length):
                self.unfragmentedAssociations[frozenset(baseClassNames)] = {}
                self.fragmentedAssociations[frozenset(baseClassNames)] = {}
                for association_length in range(1, len(classNamesIn) - base_length + 1):
                    for associatedClassNames in combinations(set(classNamesIn).difference(set(baseClassNames)),
                                                             association_length):
                        self.unfragmentedAssociations[frozenset(baseClassNames)][frozenset(associatedClassNames)] = []
                        self.fragmentedAssociations[frozenset(baseClassNames)][frozenset(associatedClassNames)] = []

        for fragmentableClass in fragmentableClassesIn:
            self.innerAssociations[frozenset([fragmentableClass])] = {}
            self.innerAssociations[frozenset([fragmentableClass])][frozenset([fragmentableClass])] = []


class ClassBasedApriori:
    def __init__(self, df, **kwargs):
        self.dataSetManager = DataSetManager(df)

        # Set support:
        supportThreshold = kwargs.get('supportThreshold', 0.001)

        # Create ItemSetTree:
        self.unfragmentedItemSetTree = ItemSetTree()
        self.fragmentedItemSetTree = ItemSetTree()
        self.innerItemSetTree = ItemSetTree()

        for index in range(self.dataSetManager.length):
            transaction = self.dataSetManager.classBasedDataSet[index]

            transactions, innertransactions = self.dataSetManager.GetFragmentedItemsets(transaction)
            for transactionToAdd in transactions:
                self.fragmentedItemSetTree.UpdateItemSetTree(transactionToAdd, index)
                if not transactionToAdd.isFragmented:
                    self.unfragmentedItemSetTree.UpdateItemSetTree(transactionToAdd, index)
            for transactionToAdd in innertransactions:
                self.innerItemSetTree.UpdateItemSetTree(transactionToAdd, index)

        # Create Associations
        self.associationManager = AssociationManager(self.dataSetManager.classNames,
                                                     self.dataSetManager.fragmentableClasses)

        for itemSet in list(self.fragmentedItemSetTree.tree.values()):
            classNames = itemSet.classBasedItemSet.classNames
            for base_length in range(1, len(classNames)):
                for baseClassNames in combinations(classNames, base_length):
                    associatedClassNames = tuple(set(classNames).difference(set(baseClassNames)))
                    support = itemSet.count / self.dataSetManager.length
                    if support < supportThreshold:
                        continue
                    baseItems = set(
                        flatten(itemSet.classBasedItemSet.uniqueNameDict[className] for className in baseClassNames))
                    associatedItems = set(
                        flatten(
                            itemSet.classBasedItemSet.uniqueNameDict[className] for className in associatedClassNames))
                    try:
                        confidence = support / self.dataSetManager.GetSupportOfItemSet(baseItems)
                    except ZeroDivisionError:
                        print("KeyError")
                    lift = confidence / self.dataSetManager.GetSupportOfItemSet(associatedItems)

                    associationToAdd = Association(baseClassNames, associatedClassNames, support, itemSet.count,
                                                   confidence,
                                                   lift, baseItems, associatedItems)
                    itemSet.AddAssociation(frozenset(baseClassNames), associationToAdd)
                    self.associationManager.fragmentedAssociations[frozenset(baseClassNames)][
                        frozenset(associatedClassNames)].append(associationToAdd)

        for itemSet in list(self.unfragmentedItemSetTree.tree.values()):
            classNames = itemSet.classBasedItemSet.classNames
            for base_length in range(1, len(classNames)):
                for baseClassNames in combinations(classNames, base_length):
                    associatedClassNames = tuple(set(classNames).difference(set(baseClassNames)))
                    support = itemSet.count / self.dataSetManager.length
                    if support < supportThreshold:
                        continue
                    baseItems = set(
                        flatten(itemSet.classBasedItemSet.uniqueNameDict[className] for className in baseClassNames))
                    associatedItems = set(
                        flatten(
                            itemSet.classBasedItemSet.uniqueNameDict[className] for className in associatedClassNames))
                    try:
                        confidence = support / self.dataSetManager.GetSupportOfItemSet(baseItems)
                    except ZeroDivisionError:
                        print("KeyError")
                    lift = confidence / self.dataSetManager.GetSupportOfItemSet(associatedItems)

                    associationToAdd = Association(baseClassNames, associatedClassNames, support, itemSet.count,
                                                   confidence, lift, baseItems, associatedItems)
                    itemSet.AddAssociation(frozenset(baseClassNames), associationToAdd)
                    self.associationManager.unfragmentedAssociations[frozenset(baseClassNames)][
                        frozenset(associatedClassNames)].append(associationToAdd)

        for itemSet in list(self.innerItemSetTree.tree.values()):
            support = itemSet.count / self.dataSetManager.length
            if support < supportThreshold:
                continue
            baseClassNames = itemSet.classBasedItemSet.classNames[0]
            associatedClassNames = itemSet.classBasedItemSet.classNames[0]
            for base_length in range(1, len(itemSet.classBasedItemSet.transactionSet)):
                for associationSet in combinations(itemSet.classBasedItemSet.uniqueNameDict[baseClassNames],
                                                   base_length):
                    baseItems = set(associationSet)
                    associatedItems = set(set(itemSet.classBasedItemSet.transactionSet).difference(baseItems))
            try:
                confidence = support / self.dataSetManager.GetSupportOfItemSet(baseItems)
                if confidence > 1:
                    continue  # duplicate items: 212
            except ZeroDivisionError:
                print("ZeroDivisionError")
            except KeyError:
                print("KeyError")
            lift = confidence / self.dataSetManager.GetSupportOfItemSet(associatedItems)

            associationToAdd = Association(baseClassNames, associatedClassNames, support, itemSet.count,
                                           confidence, lift, baseItems, associatedItems)
            itemSet.AddAssociation(frozenset(baseClassNames), associationToAdd)
            self.associationManager.innerAssociations[frozenset([baseClassNames])][
                frozenset([associatedClassNames])].append(associationToAdd)

    def CreateAssociationsToAnalyze(self, **kwargs):
        fragmentation = kwargs.get('fragmentation',
                                   'fragmentedAssociations')  # unfragmentedAssociations, innerAssociations
        baseClassNames = kwargs.get('baseClassNames', None)
        associatedClassNames = kwargs.get('associatedClassNames', None)
        condBaseItem = kwargs.get('condBaseItem', True)
        condAssociatedItem = kwargs.get('condAssociatedItem', True)
        minConfidence = kwargs.get('minConfidence', 0)
        sort = kwargs.get('sort', 'confidence')

        if baseClassNames is None:
            baseClassKeys = list(self.associationManager.__dict__[fragmentation].keys())
        else:
            baseClassKeys = []
            for baseClassName in baseClassNames:
                baseClassKeys.append(frozenset((baseClassName,)))

        if associatedClassNames is None:
            associatedClassKeys = list(self.associationManager.__dict__[fragmentation].keys())
        else:
            associatedClassKeys = []
            for associatedClassName in associatedClassNames:
                associatedClassKeys.append(frozenset((associatedClassName,)))

        associationsToReturn = []
        for key1, value1 in self.associationManager.__dict__[fragmentation].items():
            if key1 not in baseClassKeys:
                continue
            for key2, value2 in self.associationManager.__dict__[fragmentation][key1].items():
                if key2 not in associatedClassKeys:
                    continue

                associationsToReturn.append([association for association in value2
                                             if
                                             (
                                                     (condAssociatedItem is True or association.associatedItems == set(
                                                         [condAssociatedItem]))
                                                     and
                                                     (association.confidence >= minConfidence)
                                                     and
                                                     (condBaseItem is True or association.baseItems == set(
                                                         [condBaseItem]))
                                             )
                                             ]
                                            )

        associationsToReturn = flatten(associationsToReturn)
        associationsToReturn.sort(key=lambda x: x.count, reverse=True)
        associationsToReturn.sort(key=lambda x: x.__dict__[sort], reverse=True)
        return associationsToReturn

    def Plot(self, associationsIn):
        associationList = []
        for association in associationsIn:
            dictToAdd = association.__dict__.copy()
            baseItemsStr = []
            for baseItem in dictToAdd['baseItems']:
                baseItemsStr.append(self.dataSetManager.uniqueName_ItemDict[baseItem])
            dictToAdd['baseItems'] = str(baseItemsStr)
            associatedItemsStr = []
            for associatedItem in dictToAdd['associatedItems']:
                associatedItemsStr.append(self.dataSetManager.uniqueName_ItemDict[associatedItem])
            dictToAdd['associatedItems'] = str(associatedItemsStr)
            associationList.append(dictToAdd)
        dfToPlot = pd.DataFrame(associationList)
        plt.scatter(list(dfToPlot.associatedItems), list(dfToPlot.baseItems), s=list(dfToPlot.support * 90000),
                    c=list(dfToPlot.confidence), cmap="Blues", alpha=0.4, edgecolors="grey", linewidth=2, )
        plt.xticks(rotation=45)

        plt.xlabel(str(dictToAdd['associatedClassNames']), fontsize=10)
        plt.ylabel(str(dictToAdd['baseClassNames']), fontsize=10)
        plt.title(str(dictToAdd['baseClassNames']) + uniqueNameSeperator + str(dictToAdd['associatedClassNames']),
                  fontsize=14)
        plt.grid(True, 'major', ls='--')
        plt.show()

    def PlotInteractive(self, associationsIn, fileDirectory):
        dictt = {}
        for association in associationsIn:
            try:
                dictt[frozenset(association.baseItems)].append(association)
            except KeyError:
                dictt[frozenset(association.baseItems)] = [association]
        x_labels = []
        for associations in dictt.values():
            for association in associations:
                x = str(association.associatedItems)[11:-2]
                if not x_labels.__contains__(x):
                    x_labels.append(x)

        dot_chart = pygal.Dot(x_label_rotation=30)
        dot_chart.title = str(association.baseClassNames) + uniqueNameSeperator + str(association.associatedClassNames)
        dot_chart.x_labels = x_labels
        for key, value in dictt.items():
            confidenceList = [0 for i in range(len(x_labels))]
            for association in value:
                x = str(association.associatedItems)[11:-2]
                confidenceList[x_labels.index(x)] = association.confidence
            y = str(association.baseItems)[11:-2]
            dot_chart.add(y, confidenceList)
        dot_chart.render_to_file(fileDirectory)

    def Print(self, associationsIn):
        for association in associationsIn:
            print("Base items: ", association.baseItems)
            print("Associated items: ", association.associatedItems)
            print("Support: ", association.support)
            print("Confidence: ", association.confidence)
            print("Lift: ", association.lift)
            print("Count: ", association.count)
            print("-----------------------------")

    def FilterAssociations(self, associationsIn, **kwargs):
        minSupport = kwargs.get('minSupport', 0)
        minConfidence = kwargs.get('minConfidence', 0)
        minLift = kwargs.get('minLift', 0)
        minSupportQuartile = kwargs.get('minSupportQuartile', 0)
        minConfidenceQuartile = kwargs.get('minSupportQuartile', 0)
        minLiftQuartile = kwargs.get('minSupportQuartile', 0)

        sort = kwargs.get('sort', 'confidence')

        associations = associationsIn

        supportList = [x.support for x in associations]
        confidenceList = [x.confidence for x in associations]
        liftList = [x.lift for x in associations]

        supportList.sort(key=lambda x: x, reverse=True)
        confidenceList.sort(key=lambda x: x, reverse=True)
        liftList.sort(key=lambda x: x, reverse=True)

        associations = [association for association in associations
                        if
                        (
                                association.support >= supportList[int(len(supportList) * minSupportQuartile)]
                                and
                                association.confidence >= supportList[int(len(confidenceList) * minConfidenceQuartile)]
                                and
                                association.lift >= supportList[int(len(liftList) * minLiftQuartile)]
                                and
                                association.support >= minSupport
                                and
                                association.confidence >= minConfidence
                                and
                                association.lift >= minLift
                        )
                        ]

        return associations.sort(key=lambda x: x.__dict__[sort], reverse=True)

