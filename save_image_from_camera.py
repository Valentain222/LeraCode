import cv2

video_capture = cv2.VideoCapture(0)

i = int(input("first index "))
last_saved = False
while True:
    _, video_frame = video_capture.read()
    cv2.imshow("camera", video_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    elif key == ord("s") and not last_saved:
        last_saved = True
        cv2.imwrite(f"./images/img{i}.png", video_frame)
        i += 1
    else:
        last_saved = False

video_capture.release()
cv2.destroyAllWindows()