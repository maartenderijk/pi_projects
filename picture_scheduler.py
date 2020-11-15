import sched, time
from astral import LocationInfo
from astral.sun import sun, golden_hour, blue_hour, SunDirection
import datetime
from picamera import PiCamera
import glob
from PIL import Image

camera = PiCamera()
camera.resolution = (1024, 768)

def take_picture():
    now = datetime.datetime.now()
    filename = "Pi_" + now.strftime("%Y%m%d") + "_" + now.strftime("%H%M%S") + ".jpg"
    camera.capture(filename, format='jpeg', quality=100)


city = LocationInfo("Sittard", "the Netherlands", "Europe/Amsterdam", 51.001411, 5.859755)
scedule = sched.scheduler(time.time, time.sleep)

s = sun(city.observer)
gh_rise = golden_hour(city.observer)
gh_set = golden_hour(city.observer, direction=SunDirection.SETTING)
bh_rise = blue_hour(city.observer)
bh_set = blue_hour(city.observer, direction=SunDirection.SETTING)

times_rise = [s["dawn"], s["sunrise"], gh_rise[0], gh_rise[1], bh_rise[0], bh_rise[1]]
delta_rise = (max(times_rise) - min(times_rise)) // 10
intervals_rise = [min(times_rise) + (delta_rise * i) for i in range(11)]

times_set = [s["sunset"], s["dusk"], gh_set[0], gh_set[1], bh_set[0], bh_set[1]]
delta_set = (max(times_rise) - min(times_rise)) // 10
intervals_set = [min(times_rise) + (delta_set * i) for i in range(11)]


delta = datetime.timedelta(seconds=2)
intervals_test = [(datetime.datetime.now() + delta * (i+1)).timestamp() for i in range(10)]


for t in intervals_test:
    scedule.enterabs(t, 1, take_picture)

scedule.run()

fp_in = "./pi*.jpg"
fp_out = "image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=200, loop=0)