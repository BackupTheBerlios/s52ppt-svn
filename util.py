import win32api
from win32con import *

def simple_mouse(flags, x, y):
    mickey_x = x * 0x10000 / win32api.GetSystemMetrics(SM_CXSCREEN)
    mickey_y = y * 0x10000 / win32api.GetSystemMetrics(SM_CYSCREEN)
    win32api.mouse_event(flags, mickey_x, mickey_y, 0, 0)

def trim(img):
    data = list(img.getdata())
    size = img.size
    width = size[0]
    half_width = width / 2
    height = size[1]
    half_height = height / 2
    min_x, min_y, max_x, max_y = (width, height, 0, 0)
    first_pixel = data[0]

    for y in range(0, half_height - 1):
        for x in range(0, half_width - 1):
            pixel_tl = data[y*width + x]
            pixel_tr = data[y*width - x - 1]
            pixel_bl = data[(height-y-1)*width + x]
            pixel_br = data[(height-y)*width - x - 1]
            if pixel_tl != first_pixel:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
            if pixel_tr != first_pixel:
                if width - x < min_x:
                    min_x = width - x
                if width - x > max_x:
                    max_x = width - x
                if y < min_y:
                    min_y = y
                if y > max_y:
                    max_y = y
            if pixel_bl != first_pixel:
                if x < min_x:
                    min_x = x
                if x > max_x:
                    max_x = x
                if height - y < min_y:
                    min_y = height - y
                if height - y > max_y:
                    max_y = height - y
            if pixel_br != first_pixel:
                if width - x < min_x:
                    min_x = width - x
                if width - x > max_x:
                    max_x = width - x
                if height - y < min_y:
                    min_y = height - y
                if height - y > max_y:
                    max_y = height - y

    if min_x - 4 > 0:
        min_x = min_x - 4
    if min_y - 4 > 0:
        min_y = min_y - 4
    if max_x + 4 < width:
        max_x = max_x + 4
    if max_y + 4 < height:
        max_y = max_y + 4
                
    return img.crop((min_x, min_y, max_x, max_y))
