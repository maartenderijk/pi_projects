''' Automatic site update based on sensor data of raspberry pi with SENSE-hat'''
from picamera import PiCamera
from time import sleep
from sense_hat import SenseHat
from sitegenerator.sitegenerator import SiteGenerator
from datetime import datetime
import subprocess
import json

# Get Pi Photo data
now = datetime.now()
datestr = now.strftime(r"%Y%m%d%H%M%S")
img_url = "./docs/img/snap_" + datestr + ".jpg"
camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
sleep(2)
camera.capture(img_url, format='jpeg', quality=70)
camera.stop_preview()

# Get Pi sensor data
sense = SenseHat()
factor = 1.4
cpu_value = subprocess.check_output("vcgencmd measure_temp", shell=True)
cpu_temp = float(cpu_value.split("=")[1].split("'")[0])
sense_temp = sense.get_temperature()
calib_temp = round(sense_temp - ((cpu_temp - sense_temp) / factor), 1)


# Generate template for sensor data
weekdays = ("Maandag","Dinsdag","Woensdag","Donderdag","Vrijdag","Zaterdag","Zondag")
today = weekdays[datetime.today().weekday()]
now = datetime.now()

snapshot_page = SiteGenerator()
snapshot_page.base_template = "base_snapshot.html"
snapshot_page.output_file = "./templates/snapshot_" + datestr + ".html"
snapshot_page.replacements = {
    "date": today.capitalize() + " " + now.strftime(r"%d-%m-%Y"),
    "time": now.strftime(r"%H:%M:%S"),
    "temperature": str(calib_temp) + "",
    "img_url": img_url.replace("/docs","")
}
snapshot_page.render()

# Update jsonstring
json_file = "./docs/snapshots.json"
add_object = {
    "Datestring": (today.capitalize() + " " + now.strftime(r"%d-%m-%Y")), 
    "Image": img_url.replace("./docs","https://maartenderijk.github.io/sitegenerator"), 
    "Timestring": now.strftime(r"%H:%M:%S"), 
    "Temperature": calib_temp
}

with open(json_file) as f:
    data = json.load(f)

data.append(add_object)

with open(json_file, 'w') as f:
    json.dump(data, f)


# Update main template with new templates
indexpage = SiteGenerator(output_file="./docs/index.html")
indexpage.render()
