import cv2

vid = cv2.VideoCapture(1)

frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('Width x Height = ', frame_width, 'x', frame_height)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)

frame_width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('Width x Height = ', frame_width, 'x', frame_height)

ret, frame = vid.read()

if ret:
    cv2.imshow('frame',frame)
    print(frame.shape)
    vid.release()