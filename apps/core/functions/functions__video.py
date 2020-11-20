import os, cv2, math, datetime, random


def imageFromVideo(videoPath, imagePath):
    video = cv2.VideoCapture(videoPath)
    framsQty = video.get(3)
    middleFrame = int(framsQty / 2)
    count = 0
    success = 1
    while success:
        success, image = video.read()
        if count == 1:
            path = "/%s.jpg" % imagePath
            cv2.imwrite("./media/%s.jpg" % imagePath, image)
        if count >= middleFrame:
            path = "/%s.jpg" % imagePath
            cv2.imwrite("./media/%s.jpg" % imagePath, image)
            break
        count += 1
    return path

def imagePathFK(instance, filename, className = None):
    ext = filename.split('.')[-1]
    if className != None:
        path = className
    else:
        path = instance.__class__.__name__
    time = datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
    file_name = str(path).lower() + '__' + time + '__' + str(random.randrange(1000, 9999, 1))
    full_path = str(path) + '/' + str(file_name) + '.' + str(ext)
    return full_path