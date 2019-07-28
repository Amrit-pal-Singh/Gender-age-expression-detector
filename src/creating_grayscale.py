import os
import cv2
import progressbar

def new_dataset():
    cwd = os.getcwd()
    dir = os.path.join(cwd, 'male')
    print(dir)
    list = os.listdir(dir) 
    print(list)
    bar = progressbar.ProgressBar(maxval=len(list), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    per = 0
    for i in list:
        bar.update(per+1)
        per+=1
        file = os.path.join(dir, i)
        img = cv2.imread(file)
        os.remove(file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(dir, i), img)
        

def new_dataset_fe():
    cwd = os.getcwd()
    dir = os.path.join(cwd, 'female')
    print(dir)
    list = os.listdir(dir) 
    print(list)
    bar = progressbar.ProgressBar(maxval=len(list), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    per = 0
    for i in list:
        bar.update(per+1)
        per+=1
        file = os.path.join(dir, i)
        img = cv2.imread(file)
        os.remove(file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(dir, i), img)
        

new_dataset()
new_dataset_fe()