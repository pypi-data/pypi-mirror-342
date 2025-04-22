import os
import platform
import hashlib
import psutil
clientInfo={}
def init():
  memoryInfo = psutil.virtual_memory();
  clientInfo["os"] = platform.platform();
  clientInfo["memory"] = f"{memoryInfo.total/1024/1024/1024:.0f} GB";
  clientInfo["cpuCore"] = os.cpu_count();
  clientInfo["clientKey"] = hashlib.sha1(f"{os.getlogin()},{os.cpu_count(),{memoryInfo.total}}".encode("utf-8")).hexdigest().upper();
init();
