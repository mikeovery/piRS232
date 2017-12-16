import sys
import serial

cmd = sys.argv[1] + "\r\n"
match = sys.argv[2]
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1.0)
print ("Sending:" + cmd)
port.flushInput()
port.flushOutput()
port.write(cmd + " \r\n")
pdata = port.read(64)
sdata = pdata.strip().decode('UTF-8')
pos = sdata.find(match)
if pos != -1:
    len = sdata.find("\n",pos)
    if len != -1:
        print ("Data:" + sdata[pos:(len+1)])
    else:
        print ("Data:" + sdata[pos:])
else:
    print ("Returned:" + sdata)
port.close()