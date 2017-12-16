import signal
import serial
import os
import os.path
import time
from time import sleep, strftime
import argparse

parser = argparse.ArgumentParser(description='Get Controller Status')
parser.add_argument('controller', type=int, help='controller id')

args = parser.parse_args()

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
 with Timeout(5):
  done = 0
  if os.path.isfile("/home/pi/piRS232/seriallock"):
    json = '{"zones":"Locked"}'
    print (json)
    exit()
  else:
    with open("/home/pi/piRS232/seriallock", "w") as myfile:
      myfile.write('lock')
      myfile.close()

  while (done == 0):
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
    port.flushInput()
    port.flushOutput()
    data = ""
    port.write(":rzi {} \r\n".format(args.controller))
    my_logger.info("Sending: :rzi {}".format(args.controller))
    data = port.read(32)
    port.close()
    data = data.replace("\r","")
    data = data.replace("\n","")
    datapos = data.find("~:zi")
    if (datapos > -1):
        data = data[datapos:]
    if (data.split(' ')[0] == "~:zi"):
      json = '{"zones":['
      comma = ""
      ctr = 0
      for item in data.split(' '):
        if (ctr > 1) & (ctr < 8):
          json = json + comma + '{"name": "Zone' + str(ctr - 1) + '", "value":' + str(int('0x' + item, 0)) + '}'
          comma = ","
        ctr = ctr + 1
      json = json + ']}'
      print (json)
      done = 1
    else:
      #print (":".join("{:02x}".format(ord(c)) for c in data))
      port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
      port.flushInput()
      port.flushOutput()
      port.write("\r\n")
      port.close()
      sleep(1)

except Timeout.Timeout:
  json = '{"zones":"Timeout"}'
  print (json)

except:
  json = '{"zones":"Error"}'
  print (json)
	
finally:
  os.remove("/home/pi/piRS232/seriallock")
