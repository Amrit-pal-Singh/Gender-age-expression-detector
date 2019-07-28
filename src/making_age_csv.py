import os
import progressbar
import shutil
import pandas as pd


# asf (0 , 2), (4 ,  6), (8 , 12), (15 , 20), (25 , 32), (38 , 43), (48 , 53), (60 , 100)
def making_folders():
    cwd = os.getcwd()
    train = os.path.join(cwd, 'train_age')
    val = os.path.join(cwd, 'val_age')
    os.mkdir(train)
    os.mkdir(val)

    for i in range(8):
        a = os.path.join(train, str(i))
        os.mkdir(a)
    
    for i in range(8):
        a = os.path.join(val, str(i))
        os.mkdir(a)


def making_csv():
    cwd = os.getcwd()
    dirs = os.listdir(cwd)
    lines = []
    for i in dirs:
        a = i.split('_')
        if(len(a) >= 2):
            if(a[0] == 'fold'):
                file = open(i, 'r')
                l = file.readlines()
                for ii in l:
                    lines.append(str(ii))
      
    main_folder = os.path.join(cwd, 'old_train_test_val')
    sub_folder = os.listdir(main_folder)        # train, test, val
    files_names = []
    for i in sub_folder:
        s = os.path.join(main_folder, str(i))
        female_male = os.listdir(s)
        for j in female_male:
            name = os.path.join(main_folder, str(i)+'/'+str(j))
            files = os.listdir(name)
            for k in files:
                files_names.append(str(k))
    
    # (0-2)->1, (4-6)->2, (8-12)->3, (15-20)->4, (25-32)->5, (38-43)->6, (48-53)->7, (60-100)->8 
    cat = ['(0, 2)', '(4, 6)', '(8, 12)', '(8, 23)', '(15, 20)', '(25, 32)', '(27, 32)', '(38, 42)', '(38, 43)', '(38, 48)', '(48, 53)', '(60, 100)']
            # 0->1     1->2      2->3       3->4        4->4        5->5       6->5         7->6        8->6        9->6        10->7       11->8           
    age_c = []
    for i in lines:
        line = i.split('\t')
        age = line[3]
        if(age not in  age_c):
            if(len(age.split()) > 1):
                age_c.append(age)
    print(age_c)
    name_csv = []
    label_csv = []
    per = 0
    bar = progressbar.ProgressBar(maxval=len(lines), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    bar.start()
    for i in lines:
        bar.update(per+1)
        per+=1
        line = i.split('\t')
        if(len(line) < 4):
            continue
        name = line[1]
        type_ = line[2]
        age = str(line[3])
        if(age not in cat):
            continue
        fuddu = age.split()
        l = len(fuddu)
        if(l <= 1):
            continue
        else:
            for j in files_names:
                fullname = j.split('.')
                if(len(fullname) > 3):
                    a = fullname[-2]+'.jpg'
                    b = fullname[-3]
                if(a == name and b == type_):
                    name_csv.append(j)
                    if(age == cat[0]):  label_csv.append(1)
                    elif(age == cat[1]):   label_csv.append(2)
                    elif(age == cat[2]):   label_csv.append(3)
                    elif(age == cat[3] or age == cat[4]):   label_csv.append(4)
                    elif(age == cat[5] or age == cat[6] ):   label_csv.append(5)
                    elif(age == cat[7] or age == cat[8] or age == cat[9]):   label_csv.append(6)
                    elif(age == cat[10]):   label_csv.append(7)
                    elif(age == cat[11]):   label_csv.append(8)
                    else:
                        print('Fault')
                        exit(0)
        
    list_of_tuples = list(zip(name_csv, label_csv))  
    dataframe = pd.DataFrame(list_of_tuples, columns = ['name', 'label'])
    print(dataframe.head())
    dataframe.to_csv('name_label.csv', index=False)
    df = pd.read_csv('name_label.csv')
    print(df.head())



making_csv()












