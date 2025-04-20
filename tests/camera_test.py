import cv2
import time

CAMERA_DEVICES = ["/dev/video0", "/dev/video1", "/dev/video2", "/dev/video3"]

def test_camera(device):
    cap = cv2.VideoCapture(device)
    if not cap.isOpened():
        print(f"❌ {device} — не відкривається")
        return

    print(f"✅ {device} — відкрито, пробую зчитати кадр...")
    ret, frame = cap.read()
    if ret and frame is not None:
        print(f"   📷 Кадр отримано: {frame.shape}")
        cv2.imshow(f"Preview {device}", frame)
        cv2.waitKey(2000)  # показати 2 секунди
        cv2.destroyWindow(f"Preview {device}")
    else:
        print(f"⚠️ {device} — кадр не отримано")

    cap.release()

if __name__ == '__main__':
    print("\n🔍 Перевірка відеопристроїв...\n")
    for dev in CAMERA_DEVICES:
        test_camera(dev)
        time.sleep(0.5)
    print("\n✅ Завершено")
