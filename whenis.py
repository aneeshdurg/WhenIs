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
sframe = -1
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
    #For testing purposes:
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
    aPointer = 0
    thresh = 150
    a = -1
    frames[0] = 0
    ref = None
    fps = file1.get(cv2.cv.CV_CAP_PROP_FPS)
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
            cv2.destroyAllWindows()
            break
        os.system('cls')
        print str( frames[0] ) +' '+str( frames[0]/int(fps) )
        frames[0] += 1
    frame = frames[0]
    if frames[0] == 0:
        file1 = cv2.VideoCapture(vfiles[i-1])
    j = 0
    while True:
        s2, f2 = file2.read()
        d = np.sum((ref.astype('float')-f2.astype('float'))**2)
        d /= float(ref.shape[0]*ref.shape[1])
        cv2.imshow('SEARCHING', f2)
        cv2.waitKey(1)
        if d<10000:
            cv2.destroyAllWindows()
            break
        j += 1
    if j==0:
        file2 = cv2.VideoCapture(vfiles[i])
    sframe = j
    while s1 and s2: 
        s1, f1 = file1.read()
        s2, f2 = file2.read()
        if not s1 or not s2:
            aPointer = -1
            break
        cv2.imshow('f1', f1)
        d = np.sum((f1.astype('float')-f2.astype('float'))**2)
        d /= float(f1.shape[0]*f1.shape[1])
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
        print 'Frame: '+str(frame)+' Diff:'+str(d)+' Err:'+str( aPointer )+'/'+str(thresh)+' Time: '+str(frame/int(fps))
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
    print "Common matching sequence at ("+str( frames[0] )+","+str( frames[1] )+") for file "+vfiles[i-1]
    print "Common matching sequence at ("+str( sframe )+","+str( frames[1]-frames[0]+sframe )+") for file "+vfiles[i]

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
    cv2.destroyAllWindows()
    file1.release()
    file2.release()
    v.release()
    print "Found frames saved as Matching.avi"
    exit() 
