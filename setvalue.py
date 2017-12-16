import sys
import signal
import serial
import os
import os.path
import time
from time import sleep, strftime

class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass
 
    def __init__(self, sec):
        self.sec = sec
 
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)
 
    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm
 
    def raise_timeout(self, *args):
        raise Timeout.Timeout()

try:
 with Timeout(4):
  done = 0
  if os.path.isfile("/home/pi/piRS232/seriallock"):
    json = '{"data":"Locked"}'
    print (json)
    exit()
  else:
    with open("/home/pi/piRS232/seriallock", "w") as myfile:
      myfile.write('lock')
      myfile.close()

  cmd = sys.argv[1]
  cmd = cmd + " " + sys.argv[2]
  cmd = cmd + " " + sys.argv[3]
  cmd = cmd + " " + sys.argv[4]
  cmd = cmd + " " + sys.argv[5]
  cmd = cmd + " " + sys.argv[6]
  cmd = cmd + " " + sys.argv[7]
  cmd = cmd + " " + sys.argv[8]
  cmd = cmd + " " + sys.argv[9]
  cmd = cmd.replace("-","*")
  print (cmd)
  while (done == 0):
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
    port.flushInput()
    port.flushOutput()
    data = ""
    port.write(cmd + " \r\n")
    data = port.read(32)
    port.close()
    data = data.replace("\r", "")
    data = data.replace("\n", "")
    print(data)
    datapos = data.find("~1 OK")
    if (datapos > -1):
      data = data[datapos:5]
      json = '{"data":"' + data + '"}'
      #print (data)
      print (json)
      done = 1
    else:
      #print ("data: " + data)
      #print ("hex : " + ":".join("{:02x}".format(ord(c)) for c in data))
      port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
      port.flushInput()
      port.flushOutput()
      port.write("\r\n")
      port.close()
      sleep(0.5)

except Timeout.Timeout:
  json = '{"data":"TimeOut"}'
  print (json)
  data = 1

except:
  json = '{"data":"Error"}'
  print (json)
  data = 1
	
finally:
  os.remove("/home/pi/piRS232/seriallock")
