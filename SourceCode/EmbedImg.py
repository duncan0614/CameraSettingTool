# Convert an image to PNG format and embed it in a Python
# output python file as images.py

import os
import sys

def make_resources():
    try:
        from wx.tools.img2py import img2py
    except ImportError:
        print("Cannot update image resources! Using images.py from source")
        return 
    
    if sys.platform.startswith("linux") and os.getenv("DISPLAY") is None:
        print("Cannot update image resources! img2py needs X")
        return 
    
    imgDir = os.path.abspath(os.path.join("resource"))
    if not os.path.exists(imgDir):
        return

    target = os.path.abspath(os.path.join("resource", "images.py"))
    target_mtime = os.path.getmtime(target)
    
    imgResources = (
                    ("Capture", "capture.png"),
                    )
    
    for idx, (imgName, imgFile) in enumerate(imgResources):
        img2py(os.path.join(imgDir, imgFile), 
                target, append=idx>0, 
                imgName=imgName, 
                icon=True, 
                compressed=True, 
                catalog=True)

#if __name__ == '__main__':
make_resources()