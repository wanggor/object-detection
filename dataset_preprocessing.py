import os
from xml.etree.ElementTree import Element, SubElement, dump, ElementTree, parse
from shutil import copyfile, copy, move
import xml.etree.ElementTree as ET

def xml_img_checker(img_path, xml_path, output_path, show =False):
    pass

def xml_img_resize(img_path, xml_path,output_path,  copy_file = True):
    pass

def xml_class_rename(xml_path, class_name ={}, copy = True):
    file_name = []
    for r, d, f in os.walk(xml_path):
        for file in f:
            if ".xml" in file:
                path = os.path.join(r,file)
                file_name.append(path)
    for path in file_name:
        try:
            tree = parse(path)
            root = tree.getroot()
            (head, tail) = os.path.split(path)
            for object in root.findall('object'):
                name = object.find('name').text
                if name in class_name.keys():
                    name_change = class_name[name]
                    object.find('name').text = name_change
                    print(f"Renaming : {tail} : {name} to {name_change}")
            tree.write(path)
        except:
            pass

                

def xml2txt(xml_path, classname, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    xml_valid = []
    xml_notValid = []

    for r, d, f in os.walk(xml_path):
        for file in f:
            if ".xml" in file:
                path = os.path.join(r,file)
                try:
                    tree = parse(path)
                    xml_valid.append(f)
                    txt_path = os.path.join(output_path, os.path.splitext(os.path.split(path)[-1])[0]+".txt")
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
                    with open(txt_path, "w") as f:
                        for i in out:
                            text = ""
                            for n,j in enumerate(i):
                                if n == len(i)-1:
                                    text += f"{j}"
                                else:
                                    text += f"{j} "
                            text += "\n"
                            f.write(text)
                except:
                    xml_notValid.append(path)
    
    if xml_notValid != []:
        not_valit_path = os.path.join(output_path,"Not Valid")
        if not os.path.exists(not_valit_path):
            os.makedirs(not_valit_path)
        for f in xml_notValid:
            (head, tail) = os.path.split(f)
            d = os.path.join(not_valit_path, tail)
            copy(f, d)
    
    with open(os.path.join(output_path, "label.txt"), "w") as f:
        for i in classname:
            f.write(i+"\n")
    with open(os.path.join(output_path, "label.names"), "w") as f:
        for i in classname:
            f.write(i+"\n")

def txt2xml(xml_path, class_path, output_path):
    pass

if __name__ == "__main__":
    path = "annotation"
    classname = [ 'SW Asli 25','SW Asli 50', 'SW Melati 25', 'SW Murni 25']

    xml2txt(path, classname, "teks")

    xml_class_rename(path, {"SW Asli 25": "bllaslkjndknasj"})