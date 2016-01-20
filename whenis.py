import cv2
import os
import numpy as np
from sys import argv
def shift(arr, value):
    for i in range(1, len(arr)-1):
        arr[i-1] = arr[i]
    arr[len(arr)-1] = value
    return arr
def arrIsFull(arr, z):
    for i in arr:
        if (i == z).all():
            return False
    return True    
vext = ('mp4', 'mkv', 'avi') 
vDir = raw_input("Please enter the name of the directory containing the video files:\n\t")
os.chdir(vDir)
files = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]
vfiles = []
frames = [-1, -1]
for i in xrange(len(files)):
    if files[i].endswith(vext):
        vfiles.append(files[i])
fileID = 0
print "Found the following files:"
for v in vfiles:
    print v
for i in range(1,len(vfiles)):
    file1 = cv2.VideoCapture(vfiles[i-1])
    file2 = cv2.VideoCapture(vfiles[i])
    frame = 0
    s1 = True
    s2 = True
    if len(argv)!=1:
        while s1 and s2: 
            s1, f1 = file1.read()
            s2, f2 = file2.read()
            cv2.imshow('f1', f1)
            d = np.sum((f1.astype('float')-f2.astype('float'))**2)
            d /= float(f1.shape[0]*f1.shape[1])
            print str(frame)+' '+str(d)
            if frame%40 == 0:
                raw_input()
            frame += 1
            key = cv2.waitKey(1) & 0xFF 
            if key == ord('q'):
                break


        #if d>10000:
            #something = False
            #if something:
                #while True:
                    #cv2.imshow(vfiles[i-1], f1)
                    #cv2.imshow(vfiles[i], f2)
                    #key = cv2.waitKey(1) & 0xFF
                    #if key == ord('q'):
                        #break
    aPointer = 0
    thresh = 50
    a = -1
    frames[0] = 0
    ref = None
    while True:
        s1, f1 = file1.read()
        while True:
            cv2.imshow('SELECT STARTING FRAME', f1)
            key = cv2.waitKey(0) & 0xFF
            if key == ord('x'):
                ref = f1
                break
            if key == ord('n'):
                break
        if ref != None:
            break
        frames[0] += 1
    frame = frames[0]
    if frames[0] == 0:
        file1 = cv2.VideoCapture(vfiles[i-1])
    j = 0
    while True:
        s2, f2 = file2.read()
        d = np.sum((ref.astype('float')-f2.astype('float'))**2)
        d /= float(ref.shape[0]*ref.shape[1])
        if d<10000:
            break
        j += 1
    if j==0:
        file2 = cv2.VideoCapture(vfiles[i])

    #for j in xrange(1900):
    #    s1, f1 = file1.read()
    #    frame = j    
    #    s2, f2 = file2.read()
    while s1 and s2: 
        s1, f1 = file1.read()
        s2, f2 = file2.read()
        if not s1 or not s2:
            aPointer = -1
            break
        cv2.imshow('f1', f1)
        d = np.sum((f1.astype('float')-f2.astype('float'))**2)
        d /= float(f1.shape[0]*f1.shape[1])
        #print str(frame)+' '+str(d)
        #if d>10000:
            #something = False
            #if something:
                #while True:
                    #cv2.imshow(vfiles[i-1], f1)
                    #cv2.imshow(vfiles[i], f2)
                    #key = cv2.waitKey(1) & 0xFF
                    #if key == ord('q'):
                        #break
        if d<10000:
            if frames[0] == -1:
                if a!=-1:
                    frames[0] = 0
                else:
                    frames[0] = frame
            if a != -1:
                frames[1] = a
            a = -1
            aPointer = 0
            frames[1] = frame 
        else:
            if aPointer == thresh:
                break
            else:
                a = frame
                aPointer += 1
        os.system('cls')
        print str(frame)+' d:'+str(d)+' o:'+str( aPointer )+'/'+str(thresh)
        frame += 1
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    
    cv2.destroyAllWindows()
    print 'final frame count: '+str(frames[1]-frames[0])
    quit = "Terminated due to"
    if aPointer == -1:
        quit += " EOF"
    else:
        quit += " Error Threshold Reached ("+str(thresh)+")"
    print quit
    print "Common matching sequence at ("+str( frames[0] )+","+str( frames[1] )+")"
    
    file1 = cv2.VideoCapture(vfiles[0])
    for i in xrange(frames[0]):
        s, f = file1.read()
    fps = file1.get(cv2.cv.CV_CAP_PROP_FPS)
    w = file1.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    w = int(w)
    h = file1.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    h = int(h)
    v = cv2.VideoWriter('Matching.avi', cv2.cv.CV_FOURCC(*'XVID'), int(fps), (w, h), True)
    while True:
        for i in range(0, frames[1]+1-frames[0]):
            s, f = file1.read()
            cv2.imshow('frame', f)
            v.write(f)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        break   
    exit() 
