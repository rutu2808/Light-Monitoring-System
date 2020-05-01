import email_conf
from boltiot import Email, Bolt
import json, time

limit=250

mybolt= Bolt(email_conf.API_KEY, email_conf.DEVICE_ID)
mailer = Email(email_conf.MAILGUN_API_KEY, email_conf.SANDBOX_URL, email_conf.SENDER_EMAIL, email_conf.RECIPIENT_EMAIL)

while True:
	print("Reading sensor value")
	response = mybolt.analogRead('A0')
	data= json.loads(response)
	print("Sensor value is: " +str(data['value']))
	print("Getting status of LED")
	response1 = mybolt.digitalRead('0')
	data1 = json.loads(response1)
	print("Status of LED:" +str(data['value']))
	try:
		sensor_value = int(data['value'])
		status1 = int(data1['value'])
		if status1 == 0 and sensor_value < limit:
			print("Turning light on, since surrounding light reduced!")
			response = mailer.send_email("Light is turned on","Light sensor detected low light")
			response_text= json.loads(response.text)
			response=mybolt.digitalWrite('0','HIGH')
			print("Now LED is ON")
			print("Response from mailgun: " +str(response_text['message']))
	except Exception as e:
		print("Error occured: Below are the details ")
		print(e)
	time.sleep(10)