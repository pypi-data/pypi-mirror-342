import time
import json

class GameList():
    def __init__(self, list = None, expirationList = None, flippedList = None, freeze = False, deltaTime = 0):
        """
        Creates a new GameList

        Useful when you want to add, subtract, multiply, and divide items
        inside a list to calculate strength of effect or other things.
        Comes with a built-in expiration date for easy use.

        Perfect for game engine with changing stats like adding buffs and debuffs. 

        Should not receive any arguments without experienced knowledge of the library.

        Keyword arguments:
        list -- the starting list (default None)
        expirationList -- the starting list tracking expiration dates (default None)
        flippedList -- inverted list, used for faster lookup (default None)
        freeze -- preserve the list and stops the built-in expiration date deletor (default False)
        deltaTime -- tells the list how much behind it is in time. Used in updateToPresent() (default 0)
        """
        self.list: dict = list if list != None else {}
        self.expirationList: dict = expirationList if expirationList != None else {}
        self.flippedList: dict = flippedList if flippedList != None else {}

        self.addValue = 0
        self.subtractValue = 0
        self.multiplyValue = 1
        self.divideValue = 1
        self.sum = 0

        self.freeze = freeze

        self.history = [(0, {}, {}, {}, 0.0)]

        self.deltaTime = deltaTime


    def safeSum(self):
        """
        Returns the sum in a safe matter.

        Dont use this, please access the sum by using .sum
        """
        try:
            return (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue
        except ZeroDivisionError:
            print("[WARNING]: GameList can't sum the list because of a ZeroDivisionError. Defaulted the sum value to be 0.")
            return 0


    def add(self, item, expires = -1):
        """
        Adds a item to the list.

        Keyword arguments:
        item -- item you wish to add. Format: {"name":"nameHere", "type":"add/subtract/multiply/divide", "value":float}
        expires -- in seconds on how long until it expires and gets deleted. Set it to -1 to allow it to exist forever (default -1)
        """
        immortal = True if expires == -1 else False
        perf_counter = time.time()
        expires += perf_counter
        self.list[expires] = {"name":item.get("name", ""), "type":item.get("type", "add"), "value":item.get("value", 0)}


        if self.list[expires]["type"] not in ["add", "subtract", "multiply", "divide"]:
            print(f"[WARNING]: GameList only supports add/subtract/multiply/divide types. Your input type: {self.list[expires]["type"]}. Defaulting to add type.") 
            self.list[expires]["type"] = "add" 

        if not "value" in item:
            defaultValue = 0 if self.list[expires]["type"] in ["add", "subtract"] else 1
            self.list[expires]["value"] = defaultValue
            print(f"[WARNING]: GameList uses the key 'value' to store the value of each item. You seem to have not given it a value. Defaulted to {defaultValue}.") 

        if self.list[expires]["name"] == "":
            print(f'[WARNING]: GameList uses the key \'name\' to track items. You seem to have not given it a value. This will make it hard to track and pop at a later time (before its expiration date). Defaulted to "".') 

        if not immortal:
            self.expirationList[expires] = self.list[expires]
        self.flippedList[str(self.list[expires])] = expires

        if item["type"]   == "add":
            self.addValue += item["value"]
        elif item["type"] == "subtract":
            self.subtractValue += item["value"]
        elif item["type"] == "multiply":
            self.multiplyValue += (item["value"] - 1)
        elif item["type"] == "divide":
            self.divideValue += (item["value"] - 1) 

        object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))

    def unsafeAdd(self, item, expires = -1):
        """
        Adds a item to the list using a more unsafe method.

        Only use this if you know what you are doing!

        Keyword arguments:
        item -- item you wish to add. Format: {"name":"nameHere", "type":"add/subtract/multiply/divide", "value":float}
        expires -- in seconds on how long until it expires and gets deleted. Set it to -1 to allow it to exist forever (default -1)
        """
        immortal = True if expires == -1 else False
        perf_counter = time.time()
        expires += perf_counter
        self.list[expires] = item
        if not immortal:
            self.expirationList[expires] = self.list[expires]
        self.flippedList[str(item)] = expires
    
        if item["type"]   == "add":
            self.addValue += item["value"]
        elif item["type"] == "subtract":
            self.subtractValue += item["value"]
        elif item["type"] == "multiply":
            self.multiplyValue += (item["value"] - 1)
        elif item["type"] == "divide":
            self.divideValue += (item["value"] - 1)

        object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))
            

    def calculateSumWithoutUpdate(self):
        """
        Calculates the sum of the list without checking for expired items

        Use only if you want to access the sum without updating
        """
        self.addValue = 0
        self.subtractValue = 0
        self.multiplyValue = 1
        self.divideValue = 1
        for item in self.list.values():
            if item["type"]   == "add":
                self.addValue += item["value"]
            elif item["type"] == "subtract":
                self.subtractValue += item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue += (item["value"] - 1)
            elif item["type"] == "divide":
                self.divideValue += (item["value"] - 1)

        return self.safeSum()



    def update(self):
        """
        Updates the list and removes any expires items.

        This is already called upon when accessing the sum or history.
        This function doesn't need to be by the user.
        """

        # update() ignore the reeze flag because it's assumed the user is calling it with the purpose of updating it manually
        try:
            if len(self.expirationList.keys()) == 0:
                return
            expiration = min(self.expirationList.keys())
            while expiration < time.time():
                if self.list[expiration]["type"] == "add":
                    self.addValue -= self.list[expiration]["value"]
                elif self.list[expiration]["type"] == "subtract":
                    self.subtractValue -= self.list[expiration]["value"]
                elif self.list[expiration]["type"] == "multiply":
                    self.multiplyValue -= (self.list[expiration]["value"] - 1)
                else:
                    self.divideValue -= (self.list[expiration]["value"] - 1)

                del self.flippedList[str(self.list[expiration])]
                del self.list[expiration]
                del self.expirationList[expiration]

                object.__getattribute__(self, "history").append((expiration, self.list, self.expirationList, self.flippedList, self.safeSum()))
                expiration = min(self.expirationList.keys())
        except ValueError as e:
            print(f"[WARNING]: While updating the list, a new error appeared: {e}")

    def pause(self):
        """
        Prevents the list from auto-updating and prevents deletions of expired items without user input.
        """
        self.freeze = True

    def resume(self):
        """
        Resumes the list to auto-update and delete expired items automatically.
        """
        self.freeze = False

    def updateToPresent(self):
        """
        Updates each item in the list to match if the list was in the present. Setting deltaTime changes how much this affects the list.

        Only use this if you are experienced and know what you are doing.
        """
        newList = {}
        for key, value in self.list.items():
            newList[key + self.deltaTime] = value
        self.deltaTime = 0

    def restoreState(self, t) -> "GameList":
        """
        Creates a new GameList from the history of the list. Useful if you want to track previous sum values and such.

        Keyword arguments:
        t -- the time you want the new list to be based on
        """
        self.update()
        lastItem = None
        for item in self.history:
            if item[0] < t:
                lastItem = item
            else:
                break

        if lastItem == None:
            return GameList()
        else:
            return GameList(lastItem[1], lastItem[2], False, time.time() - lastItem[0])

    def getOldSums(self, t0, t1) -> list[tuple]:
        """
        Creates a list of tuples with the sum value from t0 -> t1.

        Format: [(time, sum_value), ...]

        Keyword arguments:
        t0 -- the time you want the list to start
        t1 -- the time you want the list to end
        """
        self.update()
        items = []
        for item in self.history:
            if item[0] < t0:
                items = [(item[0], item[4])]
            elif item[0] < t1:
                items.append((item[0], item[4]))
            else:
                break

        return items
        

    def pop(self, name):
        """
        Pops a item from the list with the closest expiration date to the current time

        Keyword arguments:
        name -- the name you gave the item in the list
        """
        perf_counter = time.time()
        pops = [(key, value) for key, value in self.list.items() if value["name"] == name]
        pops.sort(key=lambda a: a[0])
        if pops:
            stringedList = str(pops[0][1])

            item = self.list[self.flippedList[stringedList]]
            del self.list[self.flippedList[stringedList]]
            if self.flippedList[stringedList] in self.expirationList: del self.expirationList[self.flippedList[stringedList]]
            del self.flippedList[stringedList]

            if item["type"] == "add":
                self.addValue -= item["value"]
            elif item["type"] == "subtract":
                self.subtractValue -= item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue -= (item["value"] - 1)
            else:
                self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))

    def popAny(self, name):
        """
        Pops a item from the list with no regards for expiration date

        Keyword arguments:
        name -- the name you gave the item in the list
        """
        perf_counter = time.time()
        pops = [value for value in self.list.values() if value["name"] == name]
        if pops:
            stringedList = str(pops[0])

            item = self.list[self.flippedList[stringedList]]
            del self.list[self.flippedList[stringedList]]
            if self.flippedList[stringedList] in self.expirationList: del self.expirationList[self.flippedList[stringedList]]
            del self.flippedList[stringedList]

            if item["type"] == "add":
                self.addValue -= item["value"]
            elif item["type"] == "subtract":
                self.subtractValue -= item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue -= (item["value"] - 1)
            else:
                self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))

    def popAll(self, name):
        """
        Pops every item from the list with the given name

        Keyword arguments:
        name -- the name you gave the item(s) in the list
        """
        perf_counter = time.time()
        pops = [value for value in self.list.values() if value["name"] == name]
        if pops:
            for x in range(len(pops)):
                stringedList = str(pops[x])


                item = self.list[self.flippedList[stringedList]]
                del self.list[self.flippedList[stringedList]]
                if self.flippedList[stringedList] in self.expirationList: del self.expirationList[self.flippedList[stringedList]]
                del self.flippedList[stringedList]

                if item["type"] == "add":
                    self.addValue -= item["value"]
                elif item["type"] == "subtract":
                    self.subtractValue -= item["value"]
                elif item["type"] == "multiply":
                    self.multiplyValue -= (item["value"] - 1)
                else:
                    self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))

    def remove(self, item):
        """
        Removes a specific item from the list (if it exists)

        Keyword arguments:
        name -- the name you gave the item(s) in the list
        """
        perf_counter = time.time()
        stringedList = str(item)
        if self.flippedList.get(stringedList, None):
            del self.list[self.flippedList[stringedList]]
            if self.flippedList[stringedList] in self.expirationList: del self.expirationList[self.flippedList[stringedList]]
            del self.flippedList[stringedList]

            if item["type"] == "add":
                self.addValue -= item["value"]
            elif item["type"] == "subtract":
                self.subtractValue -= item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue -= (item["value"] - 1)
            else:
                self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))

    def unsafeRemove(self, item):
        """
        Removes a specific item from the list (if it exists)

        More unsafe compared to remove(item), so use only if you know what you are doing!

        Keyword arguments:
        name -- the name you gave the item(s) in the list
        """
        perf_counter = time.time()
        if item in self.list.values():
            stringedList = str(item)
            del self.list[dict(self.flippedList[stringedList])]
            if dict(self.flippedList[stringedList]) in self.expirationList: del self.expirationList[dict(self.flippedList[stringedList])]
            del self.flippedList[stringedList]

            if item["type"] == "add":
                self.addValue -= item["value"]
            elif item["type"] == "subtract":
                self.subtractValue -= item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue -= (item["value"] - 1)
            else:
                self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, self.safeSum()))

    def __getattribute__(self, name):
        """
        Retrieves attributes from the class

        Updates the list if you grab the sum value or the history data

        Keyword arguments:
        name -- the name of the attribute you want to grab
        """
        if name == "sum":
            if not object.__getattribute__(self, "freeze"):
                self.update()
            try:
                return (object.__getattribute__(self, "addValue") - 
                        object.__getattribute__(self, "subtractValue")) * \
                    object.__getattribute__(self, "multiplyValue") / \
                    object.__getattribute__(self, "divideValue")
            except ZeroDivisionError:
                print("[WARNING]: While retrieving the sum, a ZeroDivisionError showed up. Defaulting to 0")
                return 0
        elif name == "history":
            if not object.__getattribute__(self, "freeze"):
                self.update()


        return object.__getattribute__(self, name)
        




    