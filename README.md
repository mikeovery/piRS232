# piRS232

Allows RS232 Commands using a REST interface to a Lutron Light Controller

## Sample
[Swagger API Page](http://192.168.0.10:8080/api/v1/ui/#/) 

Pre Reqs
```
Python3
Python3-pip
Connexion
RS232 Shield
```

## Test Scripts
can be run independently using **sudo python 'scriptname' 'params'** 

**status.py**: takes 1 parameter (number of lutron contrller as a single digit)
e.g.
> pi@piname:~ $ sudo python status.py 1<br> 
> {"zones":[{"name": "Zone1", "value":0},{"name": "Zone2", "value":0},{"name": "Zone3", "value":0},{"name": "Zone4", "value":0},{"name": "Zone5", "value":0},{"name": "Zone6", "value":0}]}

## REST Interface
cd piRS232/piRS232<br>
sudo python3 app.py <br>
Access pi using your local browser http://**ip of pi**:8080/api/v1/ui/#/<br>

To run automatically add the following to the rc.local file by typing sudo nano /etc/rc.local before the exit command
>cd piRS232/piRS232<br>
>sudo python3 app.py &
