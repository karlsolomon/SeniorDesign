import cv2
print(cv2.__version__)
pathStart = "images/speed/Dustin/"
resolution = "4k/"
video = "30_Hand2/"
path = "%s%s%s" % (pathStart, resolution, video)
vidcap = cv2.VideoCapture('%s4k30fpsHand2.MOV' % path)
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  cv2.imwrite("%sframe%d.jpg" % (path, count), image)    # save frame as JPEG file
  count += 1