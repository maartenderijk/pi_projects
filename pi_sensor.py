''' Automatic site update based on sensor data of raspberry pi with SENSE-hat'''
from sense_hat import SenseHat
from sitegenerator.sitegenerator import SiteGenerator
from datetime import datetime


# Generate template for sensor data
now = datetime.now()
snapshot_page = SiteGenerator()
snapshot_page.base_template = "base_snapshot.html"
snapshot_page.output_file = "./templates/snapshot_" + now.strftime(r"%Y%m%d%H%M%S") + ".html"
snapshot_page.replacements = {
    "datetime": now.strftime(r"%Y-%m-%d %H:%M:%S"),
    "temperature": "24 C"
}
snapshot_page.render()

# Update main template with new templates
indexpage = SiteGenerator(output_file="./docs/index.html")
indexpage.render()
