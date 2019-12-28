from datetime import datetime
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)

now = datetime.now()
filename = "Pi_" + now.strftime("%Y%m%d") + "_" + now.strftime("%H%M") + ".jpg"

camera.capture(filename, format='jpeg', quality=70)
