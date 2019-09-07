''' Automatic site update based on sensor data of raspberry pi with SENSE-hat'''
from picamera import PiCamera
from time import sleep
from sense_hat import SenseHat
from sitegenerator.sitegenerator import SiteGenerator
from datetime import datetime
import subprocess

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
now = datetime.now()
snapshot_page = SiteGenerator()
snapshot_page.base_template = "base_snapshot.html"
snapshot_page.output_file = "./templates/snapshot_" + datestr + ".html"
snapshot_page.replacements = {
    "datetime": now.strftime(r"%Y-%m-%d %H:%M:%S"),
    "temperature": str(calib_temp) + " C",
    "img_url": img_url.replace("/docs","")
}
snapshot_page.render()

# Update main template with new templates
indexpage = SiteGenerator(output_file="./docs/index.html")
indexpage.render()
