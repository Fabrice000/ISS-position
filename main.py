import os
import requests
import datetime
import smtplib
import time
MY_LAT = "YOUR latitude"
MY_LONG = " YOUR longitude"
MY_EMAIL = "YOUR EMAIL"
MY_PASSWORD = os.environ.get('YOUR PASSWORD')

def iss_in_my_position():
    responce = requests.get(url="http://api.open-notify.org/iss-now.json")
    responce.raise_for_status()
    data = responce.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <=  MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    else:
        return False
def is_night():
    parameters = {
        "lat":MY_LAT,
        "lng":MY_LONG,
        "formatted":0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json",params=parameters)
    response.raise_for_status()
    data  = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    now = datetime.datetime.now()
    if now.hour >= sunset or now.hour <= sunrise:
        return True
while True:
    time.sleep(60)
    if iss_in_my_position and is_night:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user= MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,to_addrs=MY_EMAIL,msg="Subject:ISS in your position\n\nThe ISS is in your position!")
            connection.close()
        