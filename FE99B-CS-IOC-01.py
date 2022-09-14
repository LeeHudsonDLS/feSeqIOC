# Import the basic framework components.
from re import template
from softioc import softioc, builder, asyncio_dispatcher
from feSeqRecords import fvalveRecord, valveRecord
import cothread
import enum

dispatcher = asyncio_dispatcher.AsyncioDispatcher()

noOfAbsorbers = 2
dom = "FE99B"

v1 = valveRecord(f"{dom}-VA-VALVE-01")
v2 = valveRecord(f"{dom}-VA-VALVE-02")
absb1 = valveRecord(f"{dom}-RS-ABSB-01")
sht1 = valveRecord(f"{dom}-PS-SHTR-01")
sht2 = valveRecord(f"{dom}-PS-SHTR-02")
fv = fvalveRecord(f"{dom}-VA-FVALV-01")

if noOfAbsorbers > 1:
    absb2 = valveRecord(f"{dom}-RS-ABSB-02")
    absb2.addOpenRequirement(v2)
    absb2.addOpenRequirement(sht1)
    absb2.addOpenRequirement(sht2)

    absb1.addOpenRequirement(v1)
    absb1.addOpenRequirement(fv)
else:
    absb1.addOpenRequirement(v1)
    absb1.addOpenRequirement(fv)
    absb1.addOpenRequirement(sht1)
    absb1.addOpenRequirement(sht2)
    absb1.addOpenRequirement(v2)


# Create BLCON PV
builder.SetDeviceName(f"{dom}-CS-BEAM-01")
builder.mbbOut("BLCON",
                "Open",
                "Close",
                "Abort", 
                "Unknown", always_update=True,initial_value = 3)

builder.mbbOut("STA",
            "Fault",
            "Open",
            "Opening",
            "Closed",
            "Closing")



# Boilerplate get the IOC started
builder.LoadDatabase()
softioc.iocInit(dispatcher)

def update():
    toggle = 0
    while True:
        cothread.Sleep(1)


cothread.Spawn(update)
# Finally leave the IOC running with an interactive shell.
softioc.interactive_ioc(globals())