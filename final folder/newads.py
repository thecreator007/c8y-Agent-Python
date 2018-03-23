import json
import logging
import requests
import time
import configparser
import datetime

logging.basicConfig(filename='home/pi/Desktop/pro/log.log',filemode='a',format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S',level=logging.INFO)
parser =configparser.ConfigParser()
while True:
  try:
    parser.read("home/pi/Desktop/pro/parkingpi.ini")
    break
  except:
    logging.info('Could Not Read/Found The File parkingpi.ini')
    time.sleep(2)
    continue
username=parser.get('credentials','username')
password=parser.get('credentials','password')
url=parser.get('urlid','url')
url11=parser.get('urlid','url11')
url12=parser.get('urlid','url12')
url22=parser.get('urlid','url22')
urlch=parser.get('urlid','urlch')
urlme=parser.get('urlid','urlme')
head=dict(parser._sections['head'])

def check(cusdata):
  while True:
    try:
      urlchk=str(urlch+cusdata["pitype"]+"/"+cusdata["externalname"])
      s0=requests.get(urlchk,auth=(username,password),headers=head)
      s0=str(s0)
      return s0
      break
    except:
      logging.info('Could Not Check weather the Device is already available Or Not. (method : check) ')
      time.sleep(2)
      continue
def getserial():
  while True:
    try:
      did = "serialNumber"
      dr="revision"
      dmd="modelname"  
      f3 = open('/proc/cpuinfo','r')
      for line in f3:
        if line[0:6]=='Serial':
          did = line[10:26]
        if line[0:8]=='Revision':
          dr=line[10:16]
        if line[0:8]=='Hardware':
          dmd=line[10:17]
      f3.close()
      return did,dmd,dr
      break 
    except:
      time.sleep(2)
      logging.info('Could Not Get the Device Information(method : getserial')
      continue

def create_pi(pidata,cusdata):
  while True:
    try:
      s=requests.post(url,json=pidata,auth=(username,password),headers=head)
      t=s.json()
      print(s)
      idr=t["id"]
      da1={
        "type" : cusdata["pitype"],
        "externalId" :cusdata["externalname"]
      }
      url1=url11+str(idr)+url12
      s1=requests.post(url1,json=da1,auth=(username,password),headers=head)
      print(s1)
      return idr
      break 
    except:
      logging.info('Cannot Create/register the Parent Device (method : create_pi')
      time.sleep(2)
      continue

def create_dis(i,da2,cusdata):
  while True:
    try:
      da2["name"]=cusdata["sensors"][i]["name"]
      s2=requests.post(url,json=da2,auth=(username,password),headers=head)
      print(s2)
      t=s2.json()
      idd=t["id"]
      da3={
        "type" : da2["type"],
        "externalId" :da2["name"]
          }
      url1=url11+str(idd)+url12
      s3=requests.post(url1,json=da3,auth=(username,password),headers=head)
      print(s3)
      return idd
      break 
    except:
      logging.info('Cannot Create/register the child Device (method : create_dis')
      time.sleep(2)
      continue

def child_create(idr,idd):
  while True:
    try:
      url2=url+str(idr)+url22
      da4={  
          "managedObject":{"self":url+str(idd)}
      }
      s3=requests.post(url2,json=da4,auth=(username,password),headers=head)
      print(s3)
      break 
    except:
      logging.info('Cannot Create child Device (method : child_create')
      time.sleep(2)
      continue
while True:
  try:
    with open("/home/pi/Desktop/pro/parkingpi.json") as c:
      cusdata=json.load(c)
    break 
  except:
    logging.info('Cannot Read/Found the File parkingpi.json')
    time.sleep(2)
    continue

n=len(cusdata["sensors"])
s3=check(cusdata)

if s3!="<Response [200]>":
  did,dmd,dr=getserial()
  while True:
    try:
      with open('/home/pi/Desktop/pro/pidata.json') as f:
        pidata = json.load(f)
      break 
    except:
      logging.info('Cannot Read/Found the File pidata.json')
      time.sleep(2)
      continue

  pidata["name"]=cusdata["name"]
  pidata["c8y_Position"]=cusdata["location"]
  pidata["c8y_Hardware"]["serialNumber"]=did
  pidata["c8y_Hardware"]["model"]=dmd
  pidata["c8y_Hardware"]["revision"]=dr

  idr=create_pi(pidata,cusdata)
  while True:
    try:
      with open('/home/pi/Desktop/pro/disdata.json') as d:
        da2=json.load(d)
      break 
    except:
      logging.info('Cannot Read/Found the File disdata.json')
      time.sleep(2)
      continue

  idd=[0]*n 
  i=0
  while i<n:
    idd[i]=create_dis(i,da2,cusdata)
    i+=1

  i=0
  while i<n:
   child_create(idr,idd[i])
   i+=1

  i=0
  while i<n:
    add={"id":str(idd[i])}
    cusdata["sensors"][i].update(add)
    i+=1
  while True:
    try:
      with open('home/pi/Desktop/pro/sendmeasure.json', 'w') as f:
        json.dump(cusdata, f,indent=3)
      break 
    except:
      logging.info('Cannot Write To the File sendmeasure.json')
      time.sleep(2)
      continue
exec(open("home/pi/Desktop/pro/newsendmeasure.py").read())
