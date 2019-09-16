#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
# -*- coding: utf-8 -*-

import os, os.path, time
import exifread
import datetime
import platform
import sys
from PIL import Image

'''
Run:
$ python rename_pictures_in_folder.py /path/to/folder
$ python rename_pictures_in_folder.py /path/to/folder "%Y-%m-%d"
$ python rename_pictures_in_folder.py /path/to/folder "%Y-%m-%d_%H-%M-%S"

Helpful links:
- https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python/39501288#39501288
- https://timestamp.online/article/how-to-convert-timestamp-to-datetime-in-python
- https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
- https://www.pythonforbeginners.com/system/python-sys-argv
'''

def loadImages(path):
    imgs = []
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue

        full_path = os.path.join(path,f)
        image_opened = Image.open(full_path)
        imgs.append(image_opened)
    return imgs

# Extract to strategy pattern
def get_time_name_from_exif(date):
    ddate, dtime = date.split(" ", 1)
    yyyy, mm, dd = ddate.split(":", 2)
    hour, minute, second = dtime.split(":", 2)

    new_time = datetime.datetime(int(yyyy), int(mm), int(dd), int(hour), int(minute), int(second))
    
    return new_time.strftime(input_date_name_format)

# Extract to strategy pattern
def get_time_name_from_locatime(date):
    yyyy, mm, dd, hour, minute, second = time.localtime(date)[:-3]
    new_time = datetime.datetime(int(yyyy), int(mm), int(dd), int(hour), int(minute), int(second))
    
    return new_time.strftime(input_date_name_format)

def rename(images):
    total_files_not_modified = 0
    total_files_modified = 0

    for image in images:
        image_filename = image.filename

        image_file = open(image_filename, 'rb')
        tags = exifread.process_file(image_file)

        extension = os.path.splitext(image_filename)[1]

        time_name = ""

        if "EXIF DateTimeOriginal" in tags:
            date_time = str(tags["EXIF DateTimeOriginal"])
            time_name = get_time_name_from_exif(date_time)                        
        else:            
            modified = os.path.getmtime(image_filename)
            time_name = get_time_name_from_locatime(modified)

        # Example: 2013-05-05_23-20-42.jpg
        new_name = "{}/{}{}".format(root_folder, time_name, extension.lower())

        if image_filename == new_name:
            print "No changes made for:", image_filename
            total_files_not_modified += 1
        else:                
            print "From:", image_filename
            print "To:", new_name

            os.rename(image_filename, new_name)
            total_files_modified += 1

        print ""
    
    print "**************************************************************"
    print ""
    print "Total files without modification:", total_files_not_modified
    print "Total files renamed:", total_files_modified

def traverse(path):
    for dirpath, _, filenames in os.walk("."):
        for filename in [f for f in filenames if f in valid_images]:
            print dirpath
            print filename
            print os.path.join(dirpath, filename)

valid_images = [".jpg",".gif",".png",".tga", ".jpeg"]

root_folder = ""
input_date_name_format = "" 

print "Calling script with args:", sys.argv

if len(sys.argv) == 3:
    root_folder = sys.argv[1]
    input_date_name_format = sys.argv[2]
elif len(sys.argv) == 2:
    root_folder = sys.argv[1]
    input_date_name_format = "%Y-%m-%d_%H-%M-%S" 
else:
    print "MISSING ARGUMENTS"
    print "Must pass the root folder at least"
    sys.exit()

print ""
print "Renaming files at:", root_folder
print "Using date name format:", input_date_name_format
print ""
print "**************************************************************"
print ""

loaded_images = loadImages(root_folder)
rename(loaded_images)