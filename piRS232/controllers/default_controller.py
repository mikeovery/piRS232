from subprocess import *
from time import sleep, strftime
from datetime import datetime
import os.path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json
import requests

def run_cmd(cmd):
  p = Popen(cmd, shell=True, stdout=PIPE)
  output = p.communicate()[0]
  return output

def getstate(retarr, lightnum):
    ret = 0
    for x in retarr:
        if x.decode("ascii").find("lblRequest") > -1:
            data = x.decode("ascii").split(">")[1].split(" ")
            if data[lightnum] == "7f":
                ret = 1
    return ret

def ping_get() -> str:
    myjson = {}
    myjson['state'] = "OK"
    return myjson

def status_get() -> str:
    myjson = {}
    myjson['cputemp'] = round(int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3, 1)
    data = run_cmd('uptime').splitlines()[0].decode("ascii")
    myjson['uptime'] = data.split('user')[0].split(',')[0].split('up')[1].strip()
    myjson['cpuload'] = int(float(data.split('user')[1].split('average:')[1].split(',')[0].strip()) * 100)
    data = run_cmd('free').splitlines()[1].decode("ascii")
    while data.find('  ') > -1:
        data = data.replace('  ', ' ')
    myjson['memused'] = int(int(data.split(' ')[2].strip()) / 1024)
    data = run_cmd('df').splitlines()[1].decode("ascii")
    while data.find('  ') > -1:
        data = data.replace('  ', ' ')
    myjson['diskused'] = int(data.split(' ')[4].split('%')[0].strip())
    return myjson

def lutstatus1_get() -> str:
    lut = json.loads(run_cmd('sudo python /home/pi/status.py 1').splitlines()[0].decode("ascii"))
    return lut

def lutstatus_get(ctrl) -> str:
    lut = json.loads(run_cmd('sudo python /home/pi/status.py {}'.format(ctrl)).splitlines()[0].decode("ascii"))
    return lut

def lutsendszi_get(ctrl,delay,values) -> str:
    data = str(values).replace(',', ' ')
    cmd = 'sudo python /home/pi/setvalue.py :szi {} {} {}'.format(str(ctrl), str(delay), data)
    return run_cmd(cmd).splitlines()[0].decode("ascii")


def reboot_post() -> str:
    myjson = {}
    myjson['result'] = run_cmd("sudo reboot").splitlines()[0].decode("ascii")
    return myjson
    
