import cv2
print(cv2.__version__)
vidcap = cv2.VideoCapture('images/speed/5x5/IMG_7205.MOV')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  print 'Read a new frame: ', success
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1