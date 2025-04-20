import ctypes

def alert(func_name):
    ctypes.windll.user32.MessageBoxW(0, f"[!] You called '{func_name}' from FAKE cv2!", "Security Awareness", 0x40)

def imread(filename, flags=None):
    alert("imread")
    return None

def imwrite(filename, img):
    alert("imwrite")
    return True

def imshow(winname, mat=None):
    alert("imshow")

def waitKey(delay=0):
    alert("waitKey")
    return -1

def destroyAllWindows():
    alert("destroyAllWindows")

def VideoCapture(index):
    alert("VideoCapture")
    return None

def resize(src, dsize, fx=0, fy=0, interpolation=None):
    alert("resize")
    return None

def cvtColor(src, code):
    alert("cvtColor")
    return None

def GaussianBlur(src, ksize, sigmaX, sigmaY=0):
    alert("GaussianBlur")
    return None

def threshold(src, thresh, maxval, type):
    alert("threshold")
    return (None, None)

def Canny(image, threshold1, threshold2, apertureSize=3):
    alert("Canny")
    return None
