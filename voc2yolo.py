# -*- coding: utf-8 -*-

"""
Created on Mon Mar  13 15:40:43 2016
This script is to convert the txt annotation files to appropriate format needed by YOLO
@author: Martin Hwang
Email: dhhwang89@gmail.com
"""

import os
from os import walk, getcwd
import xml.etree.ElementTree as ET
import csv
from xml.etree.ElementTree import Element, SubElement, dump, ElementTree, parse

def save_txt(list_path, out_put_dir):
    for path in list_path:
        file_name = os.path.join(out_put_dir, os.path.splitext(os.path.split(path)[-1])[0]+".txt")
        tree = parse(path)
        root = tree.getroot()
        shape = {}

        for size in root.findall('size'):
            for i in size:
                shape[i.tag] = i.text
        obj = []
        for object in root.findall('object'):
            bndbox = object.find('bndbox')
            obj.append({})
            name = object.find('name').text
            obj[-1]["name"] = classname.index(name)
            for i in bndbox:
                obj[-1][i.tag] = i.text

        out = []
        for i in obj:
            dw = 1. / float(shape["width"])
            dh = 1. / float(shape["height"])

            x = (float(i["xmin"]) + float(i["xmax"])) / 2.0
            y = (float(i["ymin"]) + float(i["ymax"])) / 2.0
            w = float(i["xmax"]) - float(i["xmin"])
            h = float(i["ymax"]) - float(i["ymin"])
            x = x * dw
            w = w * dw
            y = y * dh
            h = h * dh

            out.append([i["name"], x,y,w,h])
        with open(file_name, "w") as f:
            for i in out:
                text = ""
                for n,j in enumerate(i):
                    if n == len(i)-1:
                        text += f"{j}"
                    else:
                        text += f"{j} "
                text += "\n"
                f.write(text)



if __name__ == "__main__":
    pass
    class_file = "class.names"
    xml_dir = "dataset/dataset split/wahyu/annotation"
    output_dir = "dataset/dataset split/wahyu/label"
    train = 0.7
    text_dir = "/content/darknet"

    with open(class_file) as f:
        classname = [i.strip() for i in f.readlines()]
    classname = [ 'SR Asli 25','SR Asli 50', 'SR Melati 25', 'SR Murni 25']

    list_file = []
    for r, d, f in os.walk(xml_dir):
        for file in f:
            if ".xml" in file:
                img = os.path.join(r,file)
                list_file.append(img)

    save_txt(list_file, output_dir)
