import os
from PIL import Image

from resizeimage import resizeimage
files_list = []

for root, dirs, files in os.walk('./../Aircraft/commercial-aircraft'):
    files_list.append({'commercial':files})
    #print root, dirs, files
    all_files = files

csv_str = "Image, Category\n"

for f in all_files:
    csv_str += f + ", 0\n"
    with open('./../Aircraft/commercial-aircraft/' +f, 'r+b') as i_f:
        with Image.open(i_f) as image:
            cover = resizeimage.resize_cover(image, [50, 50])
            cover.save('./../Aircraft/resized-dataset/'+f, image.format)


# save to file: file_name, 0


for root, dirs, files in os.walk('./../Aircraft/helicopter'):
    files_list.append({'commercial':files})
    all_files = files

for f in all_files:
    csv_str += f + ", 1\n"
    with open('./../Aircraft/helicopter/' +f, 'r+b') as i_f:
        with Image.open(i_f) as image:
            cover = resizeimage.resize_cover(image, [50, 50],validate=False)
            cover.save('./../Aircraft/resized-dataset/'+f, image.format)


# save to file: file_name, 1


for root, dirs, files in os.walk('./../Aircraft/military-aircraft'):
    files_list.append({'commercial':files})
    all_files = files


for f in all_files:
    csv_str += f + ", 2\n"
    with open('./../Aircraft/military-aircraft/' +f, 'r+b') as i_f:
        with Image.open(i_f) as image:
            cover = resizeimage.resize_cover(image, [50, 50],validate=False)
            cover.save('./../Aircraft/resized-dataset/'+f, image.format)

# save to file: file_name, 2

file = open('commercial.txt', 'w')
file.write(csv_str)
file.close()


