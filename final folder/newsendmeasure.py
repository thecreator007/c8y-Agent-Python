import RPi.GPIO as GPIO
import datetime

GPIO.setmode(GPIO.BCM)

def calc_distance(trig,echo):
	GPIO.setup(trig,GPIO.OUT)
	GPIO.setup(echo,GPIO.IN)

	GPIO.output(trig, False)
	time.sleep(2)

	GPIO.output(trig, True)
	time.sleep(0.00001)
	GPIO.output(trig, False)

	while GPIO.input(echo)==0:
		pulse_start = time.time()

	while GPIO.input(echo)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	return distance
while True:
	try:
		with open('/home/pi/Desktop/pro/sendmeasure.json') as jd:
			x = json.load(jd)
		break
	except:
		time.sleep(2)
		logging.info('Could Not Read/Found The File sendmeasure.json')
		continue
n=len(x["sensors"])
while True:
	i=0
	time.sleep(2)
	while i<n:
		try:
			idd = str(x["sensors"][i]["id"])
			trig = int(x["sensors"][i]["trig"])
			echo = int(x["sensors"][i]["echo"])
			dist = calc_distance(trig,echo)
			dist=275
			tim = datetime.datetime.now().isoformat()
			da={
			"source": { "id":idd  },
			"time":str(tim),
			"type": "c8y_DistanceSensor",
			"c8y_DistanceMeasurement" : {
			"distance" : { "value" : dist, "unit" : "cm" }
			}
			}
			s3=requests.post(urlme,json=da,auth=(username,password),headers=head)
			print(s3)
			i+=1
		except:
			time.sleep(2)
			logging.info('Could Send The measurement to the sensor')
			continue
GPIO.cleanup()
