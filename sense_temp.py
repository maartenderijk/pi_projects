from sense_hat import SenseHat
import subprocess

class Temperature(object):
    
    def __init__(self, factor=1.4):
        self.factor = factor
    
    def cpu_temp(self):
        cpu_temp = subprocess.check_output("vcgencmd measure_temp", shell=True)
        cpu_str = cpu_temp.split("=")[1].split("'")[0]
        return float(cpu_str)

    def sense_temp(self):
        sense = SenseHat()
        return sense.get_temperature()

    def calib_temp(self):
        return round(self.sense_temp() - ((self.cpu_temp() - self.sense_temp()) / self.factor), 1)

if __name__ == "__main__":
    t = Temperature()
    print(t.calib_temp())