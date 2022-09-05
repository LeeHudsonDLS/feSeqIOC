# Import the basic framework components.
from re import template
from softioc import softioc, builder, asyncio_dispatcher
from feSeqRecords import fvalveRecord, valveRecord
import cothread
import enum

dispatcher = asyncio_dispatcher.AsyncioDispatcher()

v1 = valveRecord("FE99I-VA-VALVE-01")
v2 = valveRecord("FE99I-VA-VALVE-02")
absb1 = valveRecord("FE99I-RS-ABSB-01")
sht1 = valveRecord("FE99I-PS-SHTR-01")
sht2 = valveRecord("FE99I-PS-SHTR-02")
fv = fvalveRecord("FE99I-VA-FVALV-01")


absb2 = valveRecord("FE99I-RS-ABSB-02",[v2,sht1,sht2])
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