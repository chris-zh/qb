from __future__ import print_function
import os, sys
from PIL import Image


# 生成压缩文件
def generate_thumbnail(infile, tag, size):
    outfile = os.path.splitext(infile)[0] + '_' + tag + ".jpg"
    imagename = outfile[len(os.path.dirname(outfile))+1:]
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, "JPEG")
        except IOError:
            print("cannot create thumbnail for", infile)
    return imagename
