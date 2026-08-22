from urllib.request import urlretrieve
import zipfile
import os

static_schedule_url = "https://svc.metrotransit.org/mtgtfs/gtfs.zip"
filename = "gtfs.zip"
target_directory = "./lib/Schedule"
download_location = os.path.join(target_directory,filename)



current_schedule_contents = os.listdir(target_directory)
for file in current_schedule_contents:
    os.remove(os.path.join(target_directory,file))
urlretrieve(static_schedule_url, download_location)

with zipfile.ZipFile(download_location, 'r') as zip_ref:
    zip_ref.extractall(target_directory)

