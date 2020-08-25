import cv2
import numpy as np
import os 

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



def main(path):
    global points
    for name in os.listdir(images_path):
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
        if len(points) != 8:
            break
        print(points)
        with open("label.txt",'a',encoding='utf8') as record:
            str1 = '{}{}'.format(name[:-3],'\t')
            for x,y in points:
                str1 += '{} {} '.format(x,y)
            str1 += '\n'
            record.write(str1)
        points = []

if __name__ == '__main__':
    images_path  = r'C:\Users\Xiahan Yang\OneDrive\work\Baidu\Baidu_OCR_blur\images'
    main(images_path)