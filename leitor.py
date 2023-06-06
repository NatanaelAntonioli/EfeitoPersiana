import cv2
import os

# ------ Constantes importantes
vidcap = cv2.VideoCapture('fps10000-rps3-boladeslz.mp4')
passo_em_frames = 4

# ------ Código

success,image = vidcap.read()

global passo
global base

count = 0
offset = 0
first_frame = True

total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = vidcap.get(cv2.CAP_PROP_FPS)
print(fps)


success, current_frame = vidcap.read()

# Produz os croppeds

while success and (offset < current_frame.shape[0] - 1):
    success, current_frame = vidcap.read()
    #cv2.imwrite("FRAMES/%d.jpg" % count, current_frame)

    if count % passo_em_frames == 0:

        cropped_image = current_frame[offset:(offset + 1), 0:current_frame.shape[1]]
        #cv2.imwrite("CROPPEDS/%d.jpg" % count, cropped_image)
            
        if first_frame:
            base = cropped_image
            first_frame = False
        else:
            base = cv2.vconcat([base, cropped_image]) 

        offset = offset + 1
    
    count = count + 1
        
cv2.imwrite("final.png", base)

