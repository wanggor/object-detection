import cv2
import os
import progressbar
import random
from shutil import copyfile, copy, move


def listvideo2image(directory, output, extention = ["MOV", "mp4"], skipframe = 10):
    startcount = 0
    for r, d, f in os.walk(directory):
        for file in f:
            if file.split(".")[-1] in extention:
                file_path = os.path.join(r, file)
                print(f"create {file} dataset ........")
                startcount = video2image(file_path,output, startcount)


def video2image(video_path, image_name, startcount= 0, skipframe = 10, format = "jpg", show = False):
    """
    convert video to image with frame step.
    """
    if not os.path.exists(image_name):
        os.makedirs(image_name)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    total_fps = int(cap.get(7)) // skipframe

    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
    
    widgets = [progressbar.FormatLabel(''),progressbar.Bar("="),"",progressbar.Percentage(), progressbar.FormatLabel('')]
    bar = progressbar.ProgressBar(total_fps+1, widgets)
    bar.start()
    
    count_frame = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            if frame_count % skipframe == 0:
                filename = os.path.join(image_name, f"{startcount}.{format}")
                cv2.imwrite(filename, frame)
                widgets[0] = progressbar.FormatLabel(f"{(count_frame)}/{(total_fps)} ")
                startcount +=1
                count_frame +=1
                widgets[-1] = progressbar.FormatLabel(f" File | {count_frame}.{format} ")
                bar.update(count_frame)
            frame_count +=1
        else:
            break
    bar.finish()
    cap.release()
    return startcount

def split_data(input_dir, output_dir, split_name = {"a": 0.7, "b":0.3}, copy_file = False, extention = ["jpg", "png"], rnd = True, size = 1):
    print("Splitting Data Started...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    list_file = []
    for r, d, f in os.walk(input_dir):
        for file in f:
            if file.split(".")[-1] in extention:
                img = os.path.join(file)
                list_file.append(img)
    
    widgets = [progressbar.FormatLabel(''),progressbar.Bar("="),"",progressbar.Percentage()]
    bar = progressbar.ProgressBar(int(len(list_file)*size), widgets)
    bar.start()

    if rnd:
        random.shuffle(list_file)
        keys = list(split_name.keys())
    else:
        list_file.sort()
        keys = list(split_name.keys()).sort()
    idx = 0
    count = 0
    list_file = list_file[0:int(len(list_file)*size)]
    
    for n, folder_name in enumerate(keys):
        max_idx = int(len(list_file) * split_name[folder_name])
        class_dir = os.path.join(output_dir, folder_name)
        
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)
        if n == len(keys)-1:
            max_idx = len(list_file) - idx

        for f in list_file[idx:idx+max_idx]:
            from_path = os.path.join(input_dir, f)
            to_path = os.path.join(class_dir, f)
            if copy_file :
                copy(from_path, to_path)
                widgets[-1] = progressbar.FormatLabel(f" Copying | {f} ")
            else:
                move(from_path, to_path)
                widgets[-1] = progressbar.FormatLabel(f" Moving| {f} ")
            count += 1
            widgets[0] = progressbar.FormatLabel(f"{(count)}/{len(list_file)} ")
            bar.update(count)
        idx = max_idx
    print("Splitting Data Complete.")

def merge_data(input_dir, output_dir,  copy_file = False, extention = ["jpg", "png"]):
    print("Merging Data Started...")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    list_file = []
    for r, d, f in os.walk(input_dir):
        for file in f:
            if file.split(".")[-1] in extention:
                img = os.path.join(r,file)
                list_file.append(img)
    
    widgets = [progressbar.FormatLabel(''),progressbar.Bar("="),"",progressbar.Percentage()]
    bar = progressbar.ProgressBar(int(len(list_file)), widgets)
    bar.start()

    count = 0
    for f in list_file:
        from_path = f
        to_path = os.path.join(output_dir,os.path.split(from_path)[-1])
        if copy_file :
            copy(from_path, to_path)
            widgets[-1] = progressbar.FormatLabel(f" Copying | {f} ")
        else:
            move(from_path, to_path)
            widgets[-1] = progressbar.FormatLabel(f" Moving| {f} ")
        count += 1
        widgets[0] = progressbar.FormatLabel(f"{(count)}/{len(list_file)} ")
        bar.update(count)

    print("Merging Data Complete.")


if __name__ == "__main__":
    #Split image Dataset
    input_directory = "dataset/image"
    output_dir = "splited_image_a"
    extention = ["jpg"]
    splited_class = {"a": 0.7, "b": 0.3}

    # split_data(input_directory, output_dir, splited_class, copy_file=True, extention=extention, rnd = True, size=0.1)
    # merge_data(output_dir, "merge", copy_file=True, extention=extention)

    input_directory = "dataset/video/ayik_1.MOV"
    # video2image(input_directory,"output")
    listvideo2image("dataset/video","output2")