from __future__ import print_function
import os, sys
from PIL import Image


# 生成压缩文件
def make_thumb(input_file, suffix, size):
    output_image = '%s%s%s%s' % (os.path.splitext(input_file)[0], '_', suffix, '.jpg')
    image_name = output_image[len(os.path.dirname(output_image)) + 1:]
    with Image.open(input_file) as im:
        im.thumbnail(size)
        im.save(output_image, 'JPEG')
    return image_name
