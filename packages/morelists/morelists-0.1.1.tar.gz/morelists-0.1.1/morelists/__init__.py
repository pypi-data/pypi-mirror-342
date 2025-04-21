import time

class GameList():
    def __init__(self, list = {}, expirationList = {}, flippedList = {}, freeze = False, deltaTime = 0):
        self.list = list
        self.expirationList = expirationList
        self.flippedList = flippedList

        self.addValue = 0
        self.subtractValue = 0
        self.multiplyValue = 1
        self.divideValue = 1
        self.sum = 0

        self.freeze = freeze

        self.history = [(0, {}, {}, {}, 0.0)]

        self.deltaTime = deltaTime


    def add(self, item, expires = -1):
        perf_counter = time.time()
        if expires != -1:
            expires += perf_counter
        self.list[expires] = {"name":item.get("name", ""), "type":item.get("type", "add"), "value":item.get("value", 0)}
        if self.list[expires]["type"] not in ["add", "subtract", "multiply", "divide"]:
            self.list[expires]["type"] = "add"

        if expires != -1:
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

        object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))

    def unsafeAdd(self, item, expires = -1):
        perf_counter = time.time()
        if expires != -1:
            expires += perf_counter
        self.list[expires] = item
        if expires != -1:
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

        object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))
            

    def calculateSum(self):
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
        return (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue



    def update(self):
        try:
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

                object.__getattribute__(self, "history").append((expiration, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))
                expiration = min(self.expirationList.keys())
        except ValueError:
            pass

    def pause(self):
        self.freeze = True

    def resume(self):
        self.freeze = False

    def updateToPresent(self):
        pass

    def restoreState(self, t) -> "GameList":
        self.update()
        lastItem = None
        for item in self.history:
            if item[0] < t:
                lastItem = item

        if lastItem == None:
            return GameList()
        else:
            return GameList(lastItem[1], lastItem[2], False, time.time() - lastItem[0])

        

    def pop(self, name):
        perf_counter = time.time()
        pops = [value for value in self.list.values() if value["name"] == name]
        pops.sort(key=lambda a: a["expires"])
        if pops:
            del self.list[self.flippedList[str(pops[0])]]
            if self.flippedList[str(pops[0])] in self.expirationList: del self.expirationList[self.flippedList[str(pops[0])]]
            del self.flippedList[str(pops[0])]
            self.calculateSum()
            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))

    def popAny(self, name):
        perf_counter = time.time()
        pops = [value for value in self.list.values() if value["name"] == name]
        if pops:
            del self.list[self.flippedList[str(pops[0])]]
            if self.flippedList[str(pops[0])] in self.expirationList: del self.expirationList[self.flippedList[str(pops[0])]]
            del self.flippedList[str(pops[0])]
            self.calculateSum()
            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))

    def popAll(self, name):
        perf_counter = time.time()
        pops = [value for value in self.list.values() if value["name"] == name]
        if pops:
            for x in range(len(pops)):
                del self.list[self.flippedList[str(pops[x])]]
                if self.flippedList[str(pops[x])] in self.expirationList: del self.expirationList[self.flippedList[str(pops[x])]]
                del self.flippedList[str(pops[x])]
                self.calculateSum()
                object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))

    def remove(self, item):
        perf_counter = time.time()
        if self.flippedList.get(str(item), None):
            del self.list[self.flippedList[str(item)]]
            if self.flippedList[str(item)] in self.expirationList: del self.expirationList[self.flippedList[str(item)]]
            del self.flippedList[str(item)]

            if item["type"] == "add":
                self.addValue -= item["value"]
            elif item["type"] == "subtract":
                self.subtractValue -= item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue -= (item["value"] - 1)
            else:
                self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))

    def unsafeRemove(self, item):
        perf_counter = time.time()
        if item in self.list.values():
            del self.list[dict(self.flippedList[str(item)])]
            if dict(self.flippedList[str(item)]) in self.expirationList: del self.expirationList[dict(self.flippedList[str(item)])]
            del self.flippedList[str(item)]

            if item["type"] == "add":
                self.addValue -= item["value"]
            elif item["type"] == "subtract":
                self.subtractValue -= item["value"]
            elif item["type"] == "multiply":
                self.multiplyValue -= (item["value"] - 1)
            else:
                self.divideValue -= (item["value"] - 1)

            object.__getattribute__(self, "history").append((perf_counter, self.list, self.expirationList, self.flippedList, (self.addValue - self.subtractValue) * self.multiplyValue / self.divideValue))

    def __getattribute__(self, name):
        if name == "sum":
            if not object.__getattribute__(self, "freeze"):
                self.update()
            return (object.__getattribute__(self, "addValue") - 
                    object.__getattribute__(self, "subtractValue")) * \
                   object.__getattribute__(self, "multiplyValue") / \
                   object.__getattribute__(self, "divideValue")
        elif name == "history":
            if not object.__getattribute__(self, "freeze"):
                self.update()


        return object.__getattribute__(self, name)
        




    