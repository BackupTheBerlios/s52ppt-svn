from win32gui import FindWindow, SetForegroundWindow
from win32con import *
from win32api import GetSystemMetrics, LoadResource
from win32com.client import Dispatch
from optparse import OptionParser
import os
import time
import util
import Image, ImageGrab
import SendKeys

PPT_HEIGHT = 554
PPT_WIDTH = 720
DEFAULT_FROM_TOP=162
DEFAULT_FROM_BOTTOM=52

def set_foreground_window(window_name):
    window = FindWindow(0, window_name)
    SetForegroundWindow(window)
    return window

def get_screen_captures(window, num_frames, from_top, from_bottom):
    screen_width = GetSystemMetrics(SM_CXSCREEN)
    screen_height = GetSystemMetrics(SM_CYSCREEN)
    box = (0, from_top, screen_width, screen_height - from_bottom)

    util.simple_mouse(MOUSEEVENTF_MOVE|MOUSEEVENTF_ABSOLUTE, screen_width / 2,\
                 screen_height / 2)
    util.simple_mouse(MOUSEEVENTF_LEFTDOWN, 0, 0)
    util.simple_mouse(MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(0.1)

    SendKeys.SendKeys("{HOME}")

    for i in range(0, num_frames):
        img = ImageGrab.grab(box)
        img = util.trim(img)
        img.save('images/image%d.png' % i)
        SendKeys.SendKeys("{DOWN}")

def create_ppt(num_slides, out_file="test.ppt"):
    pptapp = Dispatch("PowerPoint.Application")
    pptapp.Visible = True

    ppts = pptapp.Presentations.Add()
    slides = ppts.Slides

    for i in range(0, num_slides):
        slide = slides.Add(1, 12)
        img_index = num_slides - i - 1
        img = slide.Shapes.AddPicture(FileName=os.getcwd() + \
                "/images/image%d.png" % img_index, LinkToFile=False,\
                SaveWithDocument=True, Left=0, Top=0)
        img.Left = (PPT_WIDTH - img.Width) / 2
        img.Top = (PPT_HEIGHT - img.Height) / 3

    ppts.SaveAs(os.getcwd() + "/" + out_file)
    pass

if __name__ == '__main__':
    parser = OptionParser(version="%prog 1.0")
    parser.add_option("-n", "--num_slides", dest="num_slides", type="int",
                      help="Number of slides to be captured")
    parser.add_option("-t", "--title", dest="title",
                      help="Full title of the slides in Firefox")
    parser.add_option("-o", "--out_file", dest="out_file",
                      help="The output PPT file name")
    parser.add_option("-T", "--from_top", dest="from_top", type="int",
                      help="Number of pixels to be ignored from the top")
    parser.add_option("-B", "--from_bottom", dest="from_bottom", type="int",
                      help="Number of pixels to be ignored from the bottom")

    (options, args) = parser.parse_args()

    if options.num_slides == None:
        parser.error("Please input the number of slides to be captured.")
    if options.title == None:
        parser.error("Please input the full title of the slides.")

    print "Setting foreground window %s, preparing to capture slides..." % options.title

    window = set_foreground_window(options.title + " - Mozilla Firefox")

    from_top = DEFAULT_FROM_TOP
    from_bottom = DEFAULT_FROM_BOTTOM

    if options.from_top:
        from_top = options.from_top
    if options.from_bottom:
        from_bottom = options.from_bottom

    print "Capturing %d slide screen images..." % options.num_slides
    get_screen_captures(window, options.num_slides, from_top, from_bottom)

    print "Creating PPT, %d slides in total..." % options.num_slides
    create_ppt(options.num_slides)

    print "Finished converting..."
