# Replacement 
 Replace with Your hostname Instead of ***[hostname]*** in ***parkingpi.ini*** file.(Like this example-> https://example.cumulocity.com) 
 Also replace username and password of your Tenant at the place ***[username]*** and ***[password]*** Respectively in same file.

# c8y-Agent-Python
  * This fully consists of python based c8y development
  * And You Have to Gothrough the Rest Developer Section in Cumulocity Guides : https://www.cumulocity.com/guides/rest/introduction/
  * This Agent Creates ParkingPi and its child device while you run newads.py
  * This also send measurements to the c8y reading the value from the sensor using trig and echo pin and id (from the sendmeasure.json which is auto-generated) file
  