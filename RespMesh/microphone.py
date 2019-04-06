import os,subprocess,signal
import threading
import time

proc = subprocess.Popen(['bash','./recorder.sh'])
time.sleep(3)

proc.kill()
proc = subprocess.Popen(['sudo','./usbreset','/dev/bus/usb/001/011'])
time.sleep(2)
#os.kill(proc.pid, signal.SIGKILL)
proc.send_signal(signal.SIGKILL)

