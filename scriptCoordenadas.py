# objetivo line-crossing-<label>=x1d;y1d;x2d;y2d;x1c;y1c;x2c;y2c #d:direction, c:cross-line
# python3 scriptCoordenadas.py --image fyb.jpg

#  actual line (x,y) line(x,y) flecha(x,y) flecha(x,y)
import cv2 
import argparse
import numpy as np

#Parser
parser = argparse.ArgumentParser(description='Script to generate crossline coordinates')
parser.add_argument('--image', type=str, required=True, help='path to image')

global args
args = parser.parse_args() 
    
#Load Image
image = args.image
  
# read image 
#img = cv2.imread('camara10.png')
img = cv2.imread(image)  

w=img.shape[1]
h=img.shape[0]

# show image 
cv2.imshow('image', img) 
lineas=[]
puntos=[]
#print(puntos)
#print(len(puntos))
pts_array=[]
   
#define the events for the 
# mouse_click. 
def mouse_click(event, x, y,  
                flags, param): 
      
    # to check if left mouse  
    # button was clicked 
    if event == cv2.EVENT_LBUTTONDOWN: 
          
       
        # font for left click event 
        font = cv2.FONT_HERSHEY_TRIPLEX 
        puntos.append((x,y))
        #print('>>',puntos)        
        LB = str(x)+','+str(y)
          
        # display that left button  
        # was clicked. 

        #print(len(puntos))
        tam=len(puntos)
        if(tam==2 ):
            cv2.line(img, puntos[0], puntos[1], (0,255,0), 3) 

        if(tam==4 ):
            cv2.line(img, puntos[2], puntos[3], (0,255,0), 3) 
            cv2.line(img, puntos[0], puntos[3], (0,255,0), 3)
            cv2.line(img, puntos[1], puntos[3], (0,255,0), 3)

        #cv2.rectangle(img, (x, y+5), (x + 125, y - 25), (0,0,0,0), -1)
#        cv2.putText(img, LB, (x-100, y), font, 1,  (0,255, 255),1)  
        cv2.imshow('image', img) 
          
          
    # to check if right mouse  
    # button was clicked 
    if event == cv2.EVENT_RBUTTONDOWN: 
        pts_array.append(puntos.copy())
        puntos.clear()
  
cv2.setMouseCallback('image', mouse_click) 
   

while True:
    key=chr(cv2.waitKey(300) &255)
    #print (key)
    if key=='q':

        if puntos:
            pts_array.append(puntos.copy())
        for i,group in enumerate(pts_array):
            #x1d;y1d;x2d;y2d;x1c;y1c;x2c;y2c
            #current line(x,y) line(x,y) flecha(x,y) flecha(x,y)
            #print(f'group: {i}')


            #transformar  analytics 
            #QUICENTRO 640 x 480
            #PORTAL 720 X 576
            #pacifico 352 240
            #qs 640 480
            #sm 640 480
            #sl 1280 720
            points=np.array(group)
            print('shape',points.shape)
            print('points',points[:,0])
            points[:,0]=points[:,0]*640/w
            points[:,1]=points[:,1]*480/h

#**************************************
            group=points.tolist()
            
            x1d = group[2][0] 
            y1d = group[2][1] 
            x2d = group[3][0] 
            y2d = group[3][1] 
            x1c = group[0][0] 
            y1c = group[0][1] 
            x2c = group[1][0] 
            y2c = group[1][1] 

#***************************************

            print('line-crossing-i{}={};{};{};{};{};{};{};{}'.format(i,x1d,y1d,x2d,y2d,x1c,y1c,x2c,y2c))
            print('line-crossing-o{}={};{};{};{};{};{};{};{}'.format(i,x2d,y2d,x1d,y1d,x2c,y2c,x1c,y1c))
            print('width',w,'height',h)
            #print(f'line-crossing-i{i}={x1d};{y1d};{x2d};{y2d};{x1c};{y1c};{x2c};{y2c}'.format(a, b))
            #print(f'line-crossing-o{i}={x2d};{y2d};{x1d};{y1d};{x2c};{y2c};{x1c};{y1c}')
        break

    if(len(puntos)==0):
        #print('Begin line point left click')  
        #cv2.rectangle(img, (0, 0), ( 500, 50), (0,0,0), -1)
        cv2.putText(img, 'Begin line point', (0,25),  
                0, 1,  
                (0,255, 255),  
                2)  
        cv2.imshow('image', img)   
    #if(len(puntos)==1):
        #print('End line point')
    #if(len(puntos)==2):
        #print('Begin line point')

  
# close all the opened windows. 
cv2.destroyAllWindows() 




## Python code to read image
#import cv2

## To read image from disk, we use
## cv2.imread function, in below method,
#img = cv2.imread("omia_logo.png", cv2.IMREAD_COLOR)

## Creating GUI window to display an image on screen
## first Parameter is windows title (should be in string format)
## Second Parameter is image array
#cv2.imshow("Ric", img)

## To hold the window on screen, we use cv2.waitKey method
## Once it detected the close input, it will release the control
## To the next line
## First Parameter is for holding screen for specified milliseconds
## It should be positive integer. If 0 pass an parameter, then it will
## hold the screen until user close it.
#cv2.waitKey(0)

## It is for removing/deleting created GUI window from screen
## and memory
#cv2.destroyAllWindows()
