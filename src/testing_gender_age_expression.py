from fastai.vision import *
from fastai.imports import *
from pathlib import Path
import argparse
from PIL import Image
import cv2
from random import randint
from fastai.metrics import error_rate
import os



path = Path("/home/ubuntu/course-v3/nbs/dl1/datasets/basketball_watches/")

# pred_class, pred_idx, outputs = learn.predict(img)
# pred_class

def save_image(image_numpy, image_path):
    image_pil = Image.fromarray(image_numpy)
    image_pil.save(image_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='expression detector')
    parser.add_argument('--image_input', type=str)
    parser.add_argument('--video_output', type=str)
    parser.add_argument('--image_output')
    parser.add_argument('--camera', type=str)
    parser.add_argument('--model', type = str)

    args = parser.parse_args()
    if not args.image_input and not args.camera:
        print("No input image OR video")
        exit(0)
    
    cwd = os.getcwd()
    if(args.image_input):
        image = cv2.imread(args.image_input)
    
    if(args.camera):
        cam = cv2.VideoCapture(args.camera)
        ret_val, image = cam.read()
    flag = 0
    
    path = Path(cwd)    
    
    classes = ['female','male']
    data2 = ImageDataBunch.single_from_classes(path, classes = classes, size=256).normalize(imagenet_stats)
    learn = create_cnn(data2, models.resnet34)
    learn = learn.load('stage_2_gender_new_256')
    
    classes_expression = ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    data_ex = ImageDataBunch.single_from_classes(path, classes = classes_expression, size=64).normalize(imagenet_stats)
    learn_expression = create_cnn(data_ex, models.resnet34)
    learn_expression = learn_expression.load('expression_2')
    
    classes_age = [1, 2, 3, 4, 5, 6, 7]
    data_age = ImageDataBunch.single_from_classes(path, classes = classes_age, size=256).normalize(imagenet_stats)
    learn_age = create_cnn(data_age, models.resnet34)
    learn_age = learn_age.load('stage_1_age_256')
    print(image.shape)
    print(cam.get(3), cam.get(4))
        
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    if(args.video_output):
        # it will change as 
            # your phone video 4, 3
            # else 3, 4
        out = cv2.VideoWriter(args.video_output,fourcc, 20.0, (int(cam.get(3)), int(cam.get(4))))    
    
    while(True and flag == 0):
        if(args.camera):
            ret_val, image = cam.read()
        if(args.image_input):
            image = cv2.imread(args.image_input)
            flag = 1            
        # image = cv2.transpose(image)
        # image = cv2.flip(image, flipCode=0)
        
        if not len(image.shape)<3:
            image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if image is None:
            print("Wrong input image")
            exit(0)
        face_cascade_file = '/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml'
        face_cascade = cv2.CascadeClassifier(face_cascade_file)


        faces = face_cascade.detectMultiScale(
            image1, 
            scaleFactor=1.1,
            minNeighbors = 5,
            minSize = (1,1),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # print('number of faces = ', len(faces))
        for (x, y, h, w) in faces:
            rand = randint(0, 1200)
            img = image1[y:y+h, x:x+w]
            
            
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     #  
            
            
            # image_pil = pil2tensor(img, dtype=np.float32)         ##
            
            
            image_pil = Image.fromarray(img)                ##
            save_image(img, 'save.jpg')                     ##
            image_pil = open_image('save.jpg')              ##
            
            pred_class, pred_idx, outputs = learn.predict(image_pil)        
            pred_class_exp, pred_idx, outputs = learn_expression.predict(image_pil)        
            pred_age, pred_idx, outputs = learn_age.predict(image_pil)
            # cv2.imshow(('image'+str(rand)), img)
            # img = cv2.resize(img, (150, 150))
            # img = np.reshape(img, [1, 150, 150, 3])
            
            position = (int(x), int(y))
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.8
            fontColor = (0,0,255)
            lineType = 2
            # classes = model.predict_classes(img)
            p = str(pred_age)
            if(p  == '1'):
                s = "(0, 6)"
            if(p  == '2'):
                s = "(8, 12)"
            if(p  == '3'):
                s = "(15, 20)"
            if(p  == '4'):
                s = "(21 - 32)"
            if(p  == '5'):
                s = "(35 - 43)"
            if(p  == '6'):
                s = "(48 - 53)"
            if(p  == '7'):
                s = "(60 - 100)"
            
            if(str(pred_class) == 'male'):
                rec_color = (255, 0, 0)
            else:
                rec_color = (255, 255, 255)
            if(str(pred_class_exp) == 'angry'):
                fontColor = (0, 0, 255)
            else:
                fontColor = (0, 255, 0)
            cv2.rectangle(image,(x, y), (x+w, y+h), rec_color, 2)

            # print(str(pred_class))
            cv2.putText(image, str(str(pred_class)),
                position,
                font,
                fontScale, 
                fontColor, 
                lineType)
            position =  (int(x), int(y)-20)
            cv2.putText(image, str(s),
                position,
                font,
                fontScale, 
                fontColor, 
                lineType)

            position = (int(x), int(y)+20)
            cv2.putText(image, str(pred_class_exp),
                position,
                font,
                fontScale, 
                fontColor, 
                lineType)
            # print(pred_age)
                
        # cv2.resizeWindow('image', (1200, 900))
        cv2.imshow('image', image)
        if(args.image_output):
            cv2.imwrite(args.image_output, image)
        if(args.video_output):
            print(image.shape)
            out.write(image)
            
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    
    
    
    
    
    
    
    
    
    
