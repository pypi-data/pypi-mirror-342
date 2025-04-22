from . import clientInfo
import requests;
import threading
def upload_trace_log(log):

    t = threading.Thread(target=__upload,args=[log])
    t.start();

def __upload(log):
  try:
    requests.post("https://trace.clicknium.com/trace/upload",json={
      "actionPosition":log["actionPosition"],
      "message":log["message"],
      "cpuCore":f"{clientInfo['cpuCore']}",
      "os":clientInfo["os"],
      "memory":clientInfo["memory"],
      "clientKey":clientInfo["clientKey"]
    },timeout=5)
  except:
     pass;