import ndf_parse as ndf
import json
import pymongo as pymongo
from bson.json_util import dumps


class NDFMaker:
    listDivisions = []
    listDecks = []
    listStratGroups = []
    status = "not loaded"

    def __init__(self, source, destination):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = client["sean-modder"]
        self.mod = ndf.Mod(source, destination)
        self.mod.update_dst()
        pass

    def __getDeck__(self, division):
        searchMe = division.namespace
        for division in self.listDecks:
            if searchMe in division["deckCombatGroupList"]:
                return division

        return None

    def setMod(self, data):
        self.db["mods"].replace_one({"name": data["name"]}, data)

    def getMods(self):
        total = self.db["mods"].count_documents({})
        data = list(self.db["mods"].find({}))
        returnData = {
            "total": total,
            "data": data,
        }
        return dumps(returnData)
        pass

    def getModdedDecks(self, filter, limit, skip):
        total = self.db["modded-decks"].count_documents(filter)
        data = list(self.db["modded-decks"].find(filter).limit(limit).skip(skip))
        returnData = {
            "total": total,
            "data": data,
        }
        return dumps(returnData)
        pass

    def getDecks(self, filter, limit, skip):
        total = self.db["decks"].count_documents(filter)
        data = list(self.db["decks"].find(filter).limit(limit).skip(skip))
        returnData = {
            "total": total,
            "data": data,
        }
        return dumps(returnData)
        pass

    def deleteModdedDeck(self, data):
        moddedDecks = self.db["modded-decks"]
        moddedDecks.delete_one({"namespace": data})

    def makeNDF(self):
        moddedDecks = self.db["modded-decks"]
        decksToMake = list(moddedDecks.find({}))
        listofGroupsToEdit = []
        decks = self.mod.edit(
            r"GameData\Generated\Gameplay\Decks\StrategicDecks.ndf"
        ).current_tree
        groupsEdit = self.mod.edit(
            r"GameData\Generated\Gameplay\Decks\StrategicCombatGroups.ndf",
        ).current_tree

        for deck in decksToMake:
            groups = deck["groups"]
            deckPackList = deck["deckPackList"]
            deckNamespace = deck["namespace"]
            ndfDeck = decks.find_by_cond(lambda x: x.namespace == deckNamespace)
            if ndfDeck is None:
                print(f"Deck {deckNamespace} not found")
                continue
            ndfDeckUnit = ndfDeck.v.by_member("DeckPackList").v
            for i, unit in enumerate(ndfDeckUnit):
                # for unit in ndfDeckUnit:
                ndfDeckUnit.remove(i)

            for i, unit in enumerate(deckPackList):
                ndfDeckUnit.insert(i, f"~/{unit}")
            ndfDeck.v.by_member("DeckPackList").edit(ndfDeckUnit)
            listofGroupsToEdit.extend(groups)
            print("Deck updated")

        for group in listofGroupsToEdit:
            groupNamespace = group["namespace"]
            ndfGroup = groupsEdit.find_by_cond(
                lambda x: x.namespace == groupNamespace
            )
            if ndfGroup is None:
                print(f"Group {groupNamespace} not found")
                continue
            ndfGroupList = ndfGroup.v.by_member("SmartGroupList").v
            for i,smartGroup in enumerate(group["SmartGroupList"]):
                name = smartGroup["name"]
                currentSmartGroup = ndfGroupList.find_by_cond(lambda x: x.v.by_member('Name').v == name)
                if currentSmartGroup is None:
                    continue
                numbers = currentSmartGroup.v.by_member("PackIndexUnitNumberList").v
                members = smartGroup['members']
                for i, number in enumerate(numbers):
                    member = members[i]
                    number.edit((str(member['index']), str(member['numberofUnits'])))
                
            ndfGroup.v.by_member("SmartGroupList").edit(ndfGroupList)
            print("Group updated")

        for edit in self.mod.edits:
            self.mod.write_edit(edit, False)
        # with self.mod.edit(
        #     r"GameData\Generated\Gameplay\Decks\StrategicDecks.ndf"
        # ) as decks:
        #     decks.update_dst()
        #     for deck in decksToMake:
        #         deckDivision = deck["deckDivision"]
        #         groups = deck["groups"]
        #         deckPackList = deck["deckPackList"]
        #         deckNamespace = deck["namespace"]
        #         ndfDeck = decks.find_by_cond(lambda x: x.namespace == deckNamespace)
        #         if ndfDeck is None:
        #             print(f"Deck {deckNamespace} not found")
        #             continue
        #         ndfDeckUnit = ndfDeck.v.by_member("DeckPackList").v
        #         for i, unit in enumerate(ndfDeckUnit):
        #             # for unit in ndfDeckUnit:
        #             ndfDeckUnit.remove(i)

        #         for i, unit in enumerate(deckPackList):
        #             ndfDeckUnit.insert(i, f"~/{unit}")
        #         ndfDeck.v.by_member("DeckPackList").edit(ndfDeckUnit)
        #         listofGroupsToEdit.extend(groups)
        #         print("Deck updated")
        #     # self.mod.write_edit(decks)

        # pass
        # print('done')

    def saveModdedDeck(self, data):
        moddedDecks = self.db["modded-decks"]
        moddedDecks.replace_one({"namespace": data["namespace"]}, data, upsert=True)

    def __saveJson__(self):
        decks = self.db["decks"]
        decks.insert_many(self.listDecks)
        divisions = self.db["divisions"]
        divisions.insert_many(self.listDivisions)
        groups = self.db["groups"]
        groups.insert_many(self.listStratGroups)

        # Clear arrays
        self.listDecks = []
        self.listDivisions = []
        self.listStratGroups = []

    def load(self):
        self.status = "loading Divisions"
        with self.mod.edit(
            r"GameData\Generated\Gameplay\Decks\Divisions.ndf"
        ) as source:
            # find their names!
            for decks in source:
                namespace = decks.namespace
                DivisionNationalite = decks.v.by_member("DivisionNationalite").v
                self.listDivisions.append(
                    {
                        "namespace": namespace,
                        "divisionNationalite": DivisionNationalite,
                    }
                )
                pass
        self.status = "loading StrategicDecks"
        with self.mod.edit(
            r"GameData\Generated\Gameplay\Decks\StrategicDecks.ndf"
        ) as source:

            # load them into useful arrays
            for decks in source:
                deckDivision = decks.v.by_member("DeckDivision").v.replace("~/", "")

                deckCombatGroupList = decks.v.by_member("DeckCombatGroupList").v
                listGroupCombatGroups = []
                for smartGroup in deckCombatGroupList:
                    listGroupCombatGroups.append(smartGroup.value.replace("~/", ""))

                packList = decks.v.by_member("DeckPackList").v
                listPackList = []
                for smartGroup in packList:
                    listPackList.append(smartGroup.value.replace("~/", ""))

                divisionNational = None
                division = next(
                    (d for d in self.listDivisions if d["namespace"] == deckDivision),
                    None,
                )
                if division:
                    divisionNational = division["divisionNationalite"]
                    # Do something with the division
                self.listDecks.append(
                    {
                        "namespace": decks.namespace,
                        "deckDivision": deckDivision,
                        "deckCombatGroupList": listGroupCombatGroups,
                        "divisionNational": divisionNational,
                        "deckPackList": listPackList,
                    }
                )
            pass
        pass

        self.status = "loading StrategicCombatGroups"
        with self.mod.edit(
            r"GameData\Generated\Gameplay\Decks\StrategicCombatGroups.ndf"
        ) as source:
            for group_dert in source:
                smartGroupDesc = {
                    "namespace": group_dert.namespace,
                    "SmartGroupList": [],
                }

                deck = self.__getDeck__(group_dert)
                if deck is None:
                    continue
                smartGroupLists = group_dert.v.by_member("SmartGroupList")

                for smartGroup in smartGroupLists.value:
                    try:
                        members = smartGroup.v.by_member("PackIndexUnitNumberList").v

                        # this can fail!
                        smartGroupName = smartGroup.v.by_member("Name").v
                        groupSmart = {"name": smartGroupName, "members": []}

                        for number in members:
                            first = int(number.value[0])
                            unitName = deck["deckPackList"][first]
                            numberofUnits = int(int(number.value[1]))
                            groupSmart["members"].append(
                                {"unitName": unitName, "numberofUnits": numberofUnits}
                            )
                        smartGroupDesc["SmartGroupList"].append(groupSmart)
                    except Exception as e:
                        print(f"    {smartGroup.namespace} - Failed to update: {e}")
                        pass
                self.listStratGroups.append(smartGroupDesc)
            pass
        print("done loading, saving")
        self.__prepDenormal__()
        self.__saveJson__()

    def __prepDenormal__(self):
        for deck in self.listDecks:
            deck["groups"] = []
            for gl in deck["deckCombatGroupList"]:
                group = next(
                    (g for g in self.listStratGroups if g["namespace"] == gl), None
                )
                if group:
                    deck["groups"].append(group)
                pass
            pass
        pass
