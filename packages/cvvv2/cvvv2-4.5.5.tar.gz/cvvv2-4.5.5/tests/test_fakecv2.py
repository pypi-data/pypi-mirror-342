import cv2

def test_all():
    cv2.imread("image.png")
    cv2.imshow("test", None)
    cv2.waitKey()
    cv2.destroyAllWindows()
    cv2.imwrite("out.png", None)
    cv2.resize(None, (100, 100))
    cv2.cvtColor(None, 42)
    cv2.VideoCapture(0)
    cv2.GaussianBlur(None, (5, 5), 1.5)
    cv2.threshold(None, 127, 255, 0)
    cv2.Canny(None, 50, 150)
