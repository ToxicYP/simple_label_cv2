import cv2
import numpy as np
import os 
import conf as cfg 
import shutil
points = []

def on_EVENT_MOUSE(event, x, y, flags, param):
    global points
    img = param
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        points.append([x,y])
        cv2.circle(img, (x, y), 10, (255, 0, 0), thickness = -1)
        cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                    10.0, (0,0,0), thickness = 10)
        cv2.imshow("image", img)
    if event == cv2.EVENT_RBUTTONDOWN:
        x1,y1 = points.pop()
        xy = "%d,%d" % (x1, y1)
        cv2.circle(img, (x1, y1), 10, (255, 255, 255), thickness = -1)
        cv2.putText(img, xy, (x1, y1), cv2.FONT_HERSHEY_PLAIN,
                    10.0, (255,255,255), thickness = 10)
        cv2.imshow("image", img)



def points_mark(images_path,points_num):
    global points
    for root, dirs, files in os.walk(images_path):
        for name in files:
            image_name = os.path.join(images_path, name)
            image = cv2.imread(image_name)
            h,w,_ = image.shape
            # 增加cv2.WINDOW_NORMAL使生效
            cv2.namedWindow("image",cv2.WINDOW_NORMAL)
            if h>w:
                cv2.resizeWindow('image',720,960)
            else:
                cv2.resizeWindow("image",960,720)
            cv2.setMouseCallback("image",on_EVENT_MOUSE,image)
            while(1):
                cv2.imshow("image", image)
                if cv2.waitKey(0)&0xFF == 27:
                    break
            cv2.destroyAllWindows()
            if len(points) != points_num:
                break
            print(points)
            with open("label.txt",'a',encoding='utf8') as record:
                str1 = '{}{}'.format(name[:-3],'\t')
                for x,y in points:
                    str1 += '{} {} '.format(x,y)
                str1 += '\n'
                record.write(str1)
            points = []

def classify(image_path):
    line = [];
    nums = [0,0]
    break1 = False
    break2 = False
    for root,dirs,files in os.walk(image_path):
        for name in files:
            image_name = os.path.join(image_path,name)
            print(image_name)
            image = cv2.imread(image_name)
            h,w,_ = image.shape
            # 增加cv2.WINDOW_NORMAL使生效
            cv2.namedWindow("image",cv2.WINDOW_NORMAL)
            if h>w:
                cv2.resizeWindow('image',720,960)
            else:
                cv2.resizeWindow("image",960,720)
            while(1):
                cv2.imshow("image",image)
                if cv2.waitKey(0) == ord("c"):
                    dst = os.path.join("./True/",name)
                    shutil.move(image_name,dst)
                    nums[0]+=1
                    break
                elif cv2.waitKey(0) == ord("b"):
                    dst = os.path.join("./False/",name)
                    shutil.move(image_name,dst)
                    nums[1]+=1
                    break
                elif cv2.waitKey(0) == ord("d"):
                    print("Clear:{}\tBlur:{}".format(*nums))
                elif cv2.waitKey(0)&0xFF == 27:
                    break1 = True
                    break2 = True
                    break
            if break2 or nums[1]>100:
                break1 = break
                break
        if break1:
            break

if __name__ == '__main__':
    images_path  = cfg.images_path
    label_type = cfg.label_type
    if label_type == "points_mark":
        points_mark(images_path,cfg.points_num)
    elif label_type == "classify":
        classify(images_path)