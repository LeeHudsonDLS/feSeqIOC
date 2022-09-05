from time import sleep
from tkinter.messagebox import RETRY
from softioc import builder, softioc
from softioc.builder import records



class valveRecord:
    # Works for: BEAM,ABSB,SHTR,V2,
    def __init__(self,prefix,openList = list()):
        builder.SetDeviceName(prefix)
        self.openList = openList
        self.safeToOpen = False
        self.staVals = ["Fault","Open","Opening","Closed","Closing"]
        self.staPV = builder.mbbIn("STA",
                                "Fault",
                                "Open",
                                "Opening",
                                "Closed",
                                "Closing")

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
        if(self.conVals[value] == "Open"):
            self.safeToOpen = True

            if len(self.openList) > 0:
                for pv in self.openList:
                    if pv.staVals[pv.staPV.get()] != "Open":
                        self.safeToOpen = False

            if self.safeToOpen:
                self.open()
        if(self.conVals[value] == "Close"):
            self.close()
        if(self.conVals[value] == "Reset"):
            self.reset()
        self.lastConPV.set(value)



    def open(self):
        self.staPV.set(2)
        sleep(0.5)
        self.staPV.set(1)
    
    def close(self):
        self.staPV.set(4)
        sleep(0.5)
        self.staPV.set(3)

    def reset(self):
        sleep(0.5)
        self.ilkStaPV.set(2)


class fvalveRecord():
    def __init__(self,prefix):
        builder.SetDeviceName(prefix)
        self.staVals = ["Fault","Open Armed","Opening","Closed","Closing","Open Disarmed","Partially Armed"]
        self.staPV = builder.mbbIn("STA",
                                "Fault",
                                "Open Armed",
                                "Opening",
                                "Closed",
                                "Closing",
                                "Open Disarmed",
                                "Partially Armed")


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
        if(self.conVals[value] == "Arm"):
            self.arm()
        if(self.conVals[value] == "Reset"):
            self.reset()
        self.lastConPV.set(value)

    def arm(self):
        self.staPV.set(2)
        sleep(0.5)
        self.staPV.set(1)
    
    def reset(self):
        sleep(0.5)
        self.ilkStaPV.set(2)

