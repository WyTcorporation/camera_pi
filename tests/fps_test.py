import cv2
import time

cap = cv2.VideoCapture("/dev/video2")
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

start = time.time()
frames = 0

while frames < 100:
    ret, frame = cap.read()
    if ret:
        frames += 1

end = time.time()
print(f"FPS: {frames / (end - start)}")

cap.release()
