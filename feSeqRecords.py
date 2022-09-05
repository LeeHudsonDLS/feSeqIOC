from time import sleep
from tkinter.messagebox import RETRY
from softioc import builder, softioc
from softioc.builder import records



class valveRecord:
    # Works for: BEAM,ABSB,SHTR,V2,
    def __init__(self,prefix):
        builder.SetDeviceName(prefix)
        self.openList = list()
        self.observerList = list()
        self.staVals = ["Fault","Open","Opening","Closed","Closing"]
        self.staPV = builder.mbbIn("STA",
                                "Fault",
                                "Open",
                                "Opening",
                                "Closed",
                                "Closing",initial_value = 3)

        self.ilkStaVals = ["Failed","Run Ilks Ok","OK","Disarmed"]
        self.ilkStaPV = builder.mbbIn("ILKSTA",
                                "Failed",
                                "Run Ilks Ok",
                                "OK",
                                "Disarmed",initial_value = 0)

        self.conVals = ["Open","Close","Reset"]
        self.conPV = builder.mbbOut("CON",
                                "Open",
                                "Close",
                                "Reset", on_update = lambda v: self.processCommand(v), always_update=True)

        self.lastConPV = builder.mbbIn("LASTCON",
                                "Open",
                                "Close",
                                "Reset")
        self.modePV = builder.boolIn("MODE",
                                    "Operational",
                                    "Service")
        

    def processCommand(self,value):
        if self.conVals[value] == "Open":
            self.open()
        if self.conVals[value] == "Close":
            self.close()
        if self.conVals[value] == "Reset":
            self.reset()
        self.lastConPV.set(value)


    def addOpenRequirement(self,pv):
        self.openList.append(pv)
        pv.addObserver(self)

    def addObserver(self,pv):
        self.observerList.append(pv)

    def closeObservingValves(self):
        for pv in self.observerList:
            pv.reactiveClose()

    def open(self):
        if self.staVals[self.staPV.get()] != "Open" and self.ilkStaVals[self.ilkStaPV.get()] == "OK":
            self.staPV.set(2)
            sleep(0.5)
            self.staPV.set(1)
    
    def close(self):
        self.closeObservingValves()
        if self.staVals[self.staPV.get()] != "Closed":
            self.staPV.set(4)
            sleep(0.5)
            self.staPV.set(3)

    def reactiveClose(self):
        self.closeObservingValves()
        if self.staVals[self.staPV.get()] != "Closed":
            self.ilkStaPV.set(0)
            self.staPV.set(4)
            sleep(0.5)
            self.staPV.set(3)
        
        # Make interlocks fail even if valve is aleady closed
        self.ilkStaPV.set(0)

    def reset(self):
        okToReset = True
        for pv in self.openList:
            if "Open" not in pv.staVals[pv.staPV.get()]:
                okToReset = False
        
        if okToReset:
            sleep(0.5)
            self.ilkStaPV.set(2)


class fvalveRecord(valveRecord):
    def __init__(self,prefix):
        builder.SetDeviceName(prefix)
        self.openList = list()
        self.observerList = list()
        self.staVals = ["Fault","Open Armed","Opening","Closed","Closing","Open Disarmed","Partially Armed"]
        self.staPV = builder.mbbIn("STA",
                                "Fault",
                                "Open Armed",
                                "Opening",
                                "Closed",
                                "Closing",
                                "Open Disarmed",
                                "Partially Armed",initial_value = 3)


        self.ilkStaVals = ["Failed","Run Ilks Ok","OK","Disarmed"]
        self.ilkStaPV = builder.mbbIn("ILKSTA",
                                "Failed",
                                "Run Ilks Ok",
                                "OK",
                                "Disarmed",initial_value = 0)

        self.conVals = ["Open","Close","Reset","Arm","Partially Arm"]
        self.conPV = builder.mbbOut("CON",
                                "Open",
                                "Close",
                                "Reset", 
                                "Arm",
                                "Partially Arm",on_update = lambda v: self.processCommand(v), always_update=True)

        self.lastConPV = builder.mbbIn("LASTCON",
                                "Open",
                                "Close",
                                "Reset",
                                "Arm",
                                "Partially Arm")

        self.modePV = builder.boolIn("MODE",
                                    "Operational",
                                    "Service")
    


    def processCommand(self,value):
        super().processCommand(value)
        if self.conVals[value] == "Arm":
            self.arm()

    def open(self):
        if self.staVals[self.staPV.get()] != "Open" and self.ilkStaVals[self.ilkStaPV.get()] == "OK":
            self.staPV.set(2)
            sleep(0.5)
            self.staPV.set(5)

    def arm(self):
        if "Open" in self.staVals[self.staPV.get()]:
            self.staPV.set(1)
