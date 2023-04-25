import os
import json
import csv

# specify the path to the annotations directory
annotations_dir = r'C:\Users\asser\OneDrive\Desktop\prc\ann'

# specify the path to the output CSV file
output_csv = 'output.csv'

# create the CSV file and write the header row
with open(output_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['filename', 'class', 'xmin', 'ymin', 'xmax', 'ymax'])

# iterate over the annotations directory
for filename in os.listdir(annotations_dir):
    # check if the file is a JSON file
    if filename.endswith('.json'):
        # read the JSON file
        with open(os.path.join(annotations_dir, filename)) as file:
            data = json.load(file)
        # get the image filename from the JSON filename
        image_filename = filename[:-5] + '.png'
        # iterate over the bounding boxes in the JSON file
        for bbox in data['objects']:
            # get the class and bounding box coordinates
            class_name = bbox['classTitle']
            xmin = bbox['points']['exterior'][0][0]
            ymin = bbox['points']['exterior'][0][1]
            xmax = bbox['points']['exterior'][1][0]
            ymax = bbox['points']['exterior'][1][1]
            # write the data to the CSV file
            with open(output_csv, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([image_filename, class_name, xmin, ymin, xmax, ymax])
