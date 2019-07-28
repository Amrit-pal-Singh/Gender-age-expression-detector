import os, shutil
from random import randint
import shutil
import cv2

def making_folders():
    cwd = os.getcwd()
    train = os.path.join(cwd, 'train')
    test = os.path.join(cwd, 'test')
    val = os.path.join(cwd, 'val')
    os.mkdir(train)
    os.mkdir(test)
    os.mkdir(val)

    trian_female = os.path.join(train, 'female')
    test_female = os.path.join(test, 'female')
    val_female = os.path.join(val, 'female')


    trian_male = os.path.join(train, 'male')
    test_male = os.path.join(test, 'male')
    val_male = os.path.join(val, 'male')


    os.mkdir(trian_female)
    os.mkdir(test_female)
    os.mkdir(val_female)



    os.mkdir(trian_male)
    os.mkdir(test_male)
    os.mkdir(val_male)

# making of test and train
def coping_files(tt):
    cwd = os.getcwd()
    train_or_test = os.path.join(cwd, tt)
    # make a folder test and paste few folders containing pictures.
    if(tt == 'test'):
        src = os.path.join(cwd, 'aligned/test')
    else:
        src = os.path.join(cwd, 'aligned')        
    list = os.listdir(src)
    for j in list:
        if(j == 'test'):    
            continue
        images = os.listdir(src+'/'+j)
        for i in images:
            ext = i.split('.')[-1]
            if(ext == 'jpg'):
                src2 = src + '/' + j + '/' + i
                print(src2)
                shutil.copy(src2, train_or_test)


def making_test_train(tt):
    cwd = os.getcwd()
    str_m = tt+'/male'
    str_f = tt+'/female'
    male = os.path.join(cwd, str_m)
    female = os.path.join(cwd, str_f)     
    folds_dir = os.listdir(cwd)
    fold = []
    for i in folds_dir:
        if(i.split('_')[0] == 'fold'): 
            fold.append(i)
    lines = []
    for i in fold:
        file = open(i)
        lines+=file.readlines()
    print(len(lines))
    train_or_test = os.path.join(cwd, tt)
    female = os.path.join(train_or_test, 'female')
    male = os.path.join(train_or_test, 'male')
    list = os.listdir(train_or_test)
    print(len(list))
    for j in list:
        full_name = j.split('.')
        if(len(full_name) > 3):
            name = full_name[-2]+'.jpg'
            type = full_name[-3]
            # print(lines[1].split('\t')[1], lines[1].split('\t')[2])
            for i in lines:
                a = i.split('\t')[1]
                b = i.split('\t')[2]
                mf = i.split('\t')[4]
                if(name == a and type == b and mf == 'm'):
                    shutil.copy(train_or_test+'/'+j, male)
                    print(train_or_test+'/'+j,'m')
                if(name == a and type == b and mf == 'f'):
                    shutil.copy(train_or_test+'/'+j, female)
                    print(train_or_test+'/'+j,'f')
    
def delete_files(tt):
    cwd = os.getcwd()
    train_or_test = os.path.join(cwd, tt)
    list = os.listdir(train_or_test)
    for i in list:
        if(i.split('.')[-1] == 'jpg'):
            os.remove(train_or_test+'/'+i)    


def making_val():
    cwd = os.getcwd()
    train = os.path.join(cwd, 'train')
    val = os.path.join(cwd, 'val')
    female = os.path.join(train, 'female')
    male = os.path.join(train, 'male')
    vfemale = os.path.join(val, 'female')
    vmale = os.path.join(val, 'male')
    f = os.listdir(female)
    m = os.listdir(male)
    for i in range(1500):
        a = randint(0, 6000)
        # src1 = os.path.join(female, f[a])
        # if not (os.path.isfile(vfemale + '/' + f[a])):
        #     shutil.move(src1, vfemale)        
        #     print(os.path.join(vfemale, f[a]))
        src2 = os.path.join(female, f[a])
        if not os.path.isfile(vfemale + '/' + f[a]): 
            shutil.move(src2, vfemale)         
            print(os.path.join(vfemale, f[a]))

# making the file nnumber same for female and male
def twich(tt):
    cwd = os.getcwd()
    t_or_t = os.path.join(cwd, tt)
    male = os.path.join(t_or_t, 'male')
    female = os.path.join(t_or_t, 'female')
    list_m = os.listdir(male)
    list_f = os.listdir(female)
    change = len(list_m) - len(list_f)
    if(change > 0):
        lesser = 'female'
    elif(change < 0):
        lesser = 'male'
        change = -change
    else:
        print("Change not required")
        return
    print(change, lesser)
    for i in range(change):
        if(lesser == 'male'):
            list = list_m
            m_or_f = male
        else:
            list = list_f
            m_or_f = female
        rand = randint(0, len(list))
        s = os.path.join(m_or_f, list[rand])
        i = 0
        des_file = os.path.join(m_or_f, "%d%s"%(i, list[rand]))
        while(os.path.isfile(des_file)):
            i += 1
            des_file = os.path.join(m_or_f, "%d%s"%(i, list[rand]))
        print(s, des_file)
        shutil.copy(s, des_file)


def twitch_expression(tt):
    cwd = os.getcwd()
    p = os.path.join(cwd, tt)
    list_folders = os.listdir(p)
    print(list_folders)
    print(p)
    p = str(p) + '/'
    ll = []
    for i in list_folders:
        list_files = os.listdir(os.path.join(p, i))
        ll.append(len(list_files))
    m = max(ll)
    print(ll)
    print(m,'max')
    for ii in list_folders:
        print(ii,32)
        list_files = os.listdir(os.path.join(p, ii))
        num = m - len(list_files)
        print(num)
        for j in range(m - len(list_files)):
            print(p, ii)
            src = os.path.join(str(p), str(ii))
            rand = randint(0, len(list_files)-100)
            s = os.path.join(src, list_files[rand])
            i = 0
            des_file = os.path.join(src, "%d%s"%(i, list_files[rand]))
            while(os.path.isfile(des_file)):
                i += 1
                des_file = os.path.join(src, "%d%s"%(i, list_files[rand]))
            print(s, des_file)
            shutil.copy(s, des_file)

def convert_to_gray():
    cwd = os.getcwd()
    dir = os.path.join(cwd, 'old_train_test_val')
    dir = os.path.join(dir, 'train/male')
    print(dir)
    list = os.listdir(dir)
    img = cv2.imread(dir+'/'+list[0])
    if(img is None):
        print("image not loaded")
        return 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('image', gray)
    if(cv2.waitKey(0) == 27):
        return


if __name__ == "__main__":
    # making_test_train('train')
    # making_test_train('test')    
    # delete_files('train')
    # delete_files('test')
    # making_folders()
    # coping_files('test')
    # making_val()
    #twitch_expression('expression/validation')
    twich('old_train_test_val/train')







