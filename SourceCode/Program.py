"""
Copyright (c) 2022 SINBON Electronics Co., Ltd.
Design & Development by EMS DDE320

Main program
Python Version:3.9.13
IDE:Visual Studio Code 1.68.0

Module list:
# GUI module
wxPython 4.1.1
#subscript/publish module
Pypubsub 4.0.3
# build exe module
pyinstaller 5.0.1
#Web API module
requests 2.27.1
# VISA,GPIB,RS232 module
PyVISA 1.12.0

# get mac address module
pywin32-304
wmi-1.5.1

# get NTP Server time module
ntplib 0.4.0
# keyboard event modlue
pynput  1.7.6

# hid usb modlue
need to install NI-VISA driver first
https://www.ni.com/zh-tw/support/downloads/drivers/download.ni-visa.html#460225
pywinusb 0.4.2

# support function overload
multipledispatch 0.6.0

# pyserial 3.5
# crccheck 1.1
"""

import wx
from CameraMainFrame import CameraSetting

class Program():

    _instance = None

    @staticmethod
    def Instance():
        if Program._instance is None:
            Program()
        return Program._instance

    def __init__(self):
        if Program._instance is None:
            self._id = id(self)
            Program._instance = self      

    def IsAppRunning(self):
        self.name = "A9314398_EDI_UploadGTW"
        self.instance = wx.SingleInstanceChecker(self.name, path='lockfiles') # actually path isn't used in Win32
        if self.instance.IsAnotherRunning():
            wx.MessageBox("The " + self.name + " application is already running.", "Warning", wx.OK | wx.ICON_WARNING)
            return True

        self.CameraSetting = CameraSetting(None)

        return False 

if __name__ == '__main__':
    app = wx.App()
    if not Program.Instance().IsAppRunning():
        app.MainLoop()
