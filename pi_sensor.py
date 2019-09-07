''' Automatic site update based on sensor data of raspberry pi with SENSE-hat'''
from picamera import PiCamera
from time import sleep
from sense_hat import SenseHat
from sitegenerator.sitegenerator import SiteGenerator
from datetime import datetime


# Get Pi Sensor data
now = datetime.now()
datestr = now.strftime(r"%Y%m%d%H%M%S")
img_url = "./docs/img/snap_" + datestr + ".jpg"
camera = PiCamera()
camera.resolution = (640, 480)
camera.start_preview()
sleep(2)
camera.capture(img_url)
camera.stop_preview()


# Generate template for sensor data
now = datetime.now()
snapshot_page = SiteGenerator()
snapshot_page.base_template = "base_snapshot.html"
snapshot_page.output_file = "./templates/snapshot_" + datestr + ".html"
snapshot_page.replacements = {
    "datetime": now.strftime(r"%Y-%m-%d %H:%M:%S"),
    "temperature": "24 C",
    "img_url": img_url.replace("/docs","")
}
snapshot_page.render()

# Update main template with new templates
indexpage = SiteGenerator(output_file="./docs/index.html")
indexpage.render()
