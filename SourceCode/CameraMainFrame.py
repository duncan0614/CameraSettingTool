import resource.images as resImg
import cv2
import wmi, os # numpy
import threading
# from winreg import *
from datetime import datetime
import wx
from CameraSettingDialog import SettingDialog
from CameraParameter import CurrentParameter
from WxGenStaticBitmap import GenStaticBitmap

class CameraSetting (wx.Frame):
    
    camera = None
    cameraStop = True
    cameraImg = None
    picHSV = False
    waitCameraSetting = False
    currentParameter = CurrentParameter()
    picture = None

    def __init__(self, parent):
        # Note: set the frame without maximum and minimize
        super(CameraSetting, self).__init__(parent, title="MainFrame", size=wx.Size(1000, 650), style=wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.SetMinSize(wx.Size(1000, 650))
        self.SetMaxSize(wx.Size(1000, 650))
        
        self.InitUI()
        self.InitMenu()
        self.Centre()
        self.Show()
        self.OpenCamera()

    def InitUI(self):
        
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Note: Create a black buffer image
        # blackImage = numpy.zeros((550, 850, 4), dtype = numpy.uint8)
        # self.bmp1 = wx.Bitmap.FromBuffer(850, 550, blackImage)
        
        # Note: Create a transparent bitmap
        self.transparent = wx.Bitmap.FromRGBA(850, 550, 0, 0, 0, wx.ALPHA_TRANSPARENT)

        self.picturebox = GenStaticBitmap(panel, -1, size = (850, 550), bitmap = self.transparent)
        hbox.Add(self.picturebox, flag = wx.ALIGN_CENTER | wx.LEFT | wx.RIGHT, border = 20)

        # Note: Search all the camera in the PC
        CameraIndexList = self.FindCameraIndex("")

        # Combo box for camera index
        self.cbox = wx.ComboBox(panel, choices=CameraIndexList, size=(75, 40), style=wx.CB_READONLY)
        if len(CameraIndexList) == 0:
            wx.MessageBox("You don't have any camera!!")
        else:
            self.cbox.SetSelection(0)
        vbox.Add(self.cbox, flag = wx.BOTTOM, border = 190)      

        # Capture button
        self.btncapture = wx.Button(panel, size=(75, 40))
        
        # Set picture into the button
        img = wx.Bitmap.ConvertToImage(resImg.Capture.Bitmap)
        height = self.btncapture.Size.Height/img.GetHeight()
        width = self.btncapture.Size.Width/img.GetWidth()
        ratio = min(height,width)

        bitmap = img.Scale(int(img.GetHeight()*ratio),int(img.GetWidth()*ratio)).ConvertToBitmap()
        self.btncapture.SetBitmap(bitmap)
        vbox.Add(self.btncapture, flag = wx.BOTTOM, border = 160)
       
        self.btnalbum = wx.Button(panel, size = (90, 115))

        # Set picture into the button
        if os.path.exists("Pictures"):
            ret = os.listdir("Pictures")
            if len(ret) == 0:
                img = wx.Bitmap.ConvertToImage(self.transparent)
                self.btnalbum.Enable(False)
            else:
                img = wx.Image(f"Pictures\\{ret[0]}")
                self.btnalbum.Enable(True)
        else:
            img = wx.Bitmap.ConvertToImage(self.transparent)
            self.btnalbum.Enable(False)
        
        height = self.btnalbum.Size.Height/img.GetHeight()
        width = self.btnalbum.Size.Width/img.GetWidth()
        ratio = min(height,width)

        bitmap = img.Scale(int(img.GetHeight()*ratio),int(img.GetWidth()*ratio)).ConvertToBitmap()
        self.btnalbum.SetBitmap(bitmap)
        vbox.Add(self.btnalbum, flag = wx.BOTTOM, border = 0)

        # set sizer
        hbox.Add(vbox, flag = wx.ALIGN_CENTER | wx.Right, border = 20)       
        panel.SetSizer(hbox)

        # Bind Event
        self.Bind(wx.EVT_BUTTON, self.CameraCapture, self.btncapture)
        self.Bind(wx.EVT_BUTTON, self.Openalbum, self.btnalbum)
        self.Bind(wx.EVT_TEXT, self.ComboChange, self.cbox)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
 
    def FindCameraIndex(self, name:str) -> int:
        cameraindexlist = self.GetCameraData()

        # can not find Camera name
        return cameraindexlist

    def GetCameraData(self) -> list:
        query = wmi.WMI()
        cameraindexlist = []

        # query camera device list by PNPClass
        index = 0
        for pnp in query.Win32_PnPEntity():
            if pnp.PNPClass == 'Image' or pnp.PNPClass == 'Camera':
                # print(pnp.Name,":",pnp.DeviceID)
                cameraindexlist.append(str(index))
                index += 1

        # print(cameraindexlist)
        return cameraindexlist
    
    def ComboChange(self, event):  
        self.cbox.Enable(False)
        self.btncapture.Enable(False)
        if self.cbox.GetValue() == self.cameraindex:
            self.cbox.Enable(True)
            self.btncapture.Enable(True)
            return
        
        self.cameraStop = True
        self.camerathread.join()

        self.OpenCamera()
        self.cbox.Enable(True)
        self.btncapture.Enable(True)

    def CameraCapture(self, event):
        self.cbox.Enable(False)
        self.btncapture.Enable(False)
        nowTime = datetime.now()
        if not os.path.exists("Pictures"):
                os.mkdir("Pictures")
        cv2.imwrite(f"Pictures\\{nowTime.strftime('%Y%m%d%H%M%S')}.jpg", self.cameraImg)

        img = wx.Image(f"Pictures\\{nowTime.strftime('%Y%m%d%H%M%S')}.jpg")
        height = self.btnalbum.Size.Height/img.GetHeight()
        width = self.btnalbum.Size.Width/img.GetWidth()
        ratio = min(height,width)

        bitmap = img.Scale(int(img.GetHeight()*ratio),int(img.GetWidth()*ratio)).ConvertToBitmap()

        self.btnalbum.SetBitmap(bitmap)
        self.btnalbum.Enable(True)

        self.cbox.Enable(True)
        self.btncapture.Enable(True)

    def Openalbum(self, event):
        if os.path.exists("Pictures"):
            os.startfile("Pictures")
        else:
            self.btnalbum.Enable(False)
            img = wx.Bitmap.ConvertToImage(self.transparent)
            height = self.btnalbum.Size.Height/img.GetHeight()
            width = self.btnalbum.Size.Width/img.GetWidth()
            ratio = min(height,width)

            bitmap = img.Scale(int(img.GetHeight()*ratio),int(img.GetWidth()*ratio)).ConvertToBitmap()
            self.btnalbum.SetBitmap(bitmap)
            
            wx.MessageBox("Cannot find Pictures folder!",'Warning',wx.OK | wx.ICON_WARNING)

    def OnCloseWindow(self, event):
        self.cameraStop = True
        self.Destroy()

    def InitMenu(self):

        menubar = wx.MenuBar()
        
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        menubar.SetFont(font)

        FileMenu = wx.Menu()
        menubar.Append(FileMenu, '&File')
        ExitItem = wx.MenuItem(FileMenu, 5, '&Exit')
        ExitItem.SetFont(font)
        FileMenu.Append(ExitItem)

        CameraMenu = wx.Menu()
        menubar.Append(CameraMenu, '&Camera')
        AdjustItem = wx.MenuItem(CameraMenu, 6, '&Adjust')
        AdjustItem.SetFont(font)
        CameraMenu.Append(AdjustItem)

        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.CloseFrame, ExitItem)
        self.Bind(wx.EVT_MENU, self.OpenDialog, AdjustItem)

    def CloseFrame(self, event):
        self.cameraStop = True
        self.Close()

    def OpenDialog(self, event):
        self.dialog = SettingDialog(self)
        self.dialog.ShowModal()
        self.dialog.Destroy()
    
    def OpenCamera(self):
        try:
            self.cameraindex = self.cbox.GetValue()
            if self.cameraindex == '':
                return
            
            self.camera = cv2.VideoCapture(int(self.cameraindex), cv2.CAP_DSHOW)
            if not self.camera.isOpened():
                wx.MessageBox("Camera open failed.")
                return

            self.cameraStop = False
            self.camerathread = threading.Thread(target=self.CameraOutput)
            self.camerathread.start()

        except Exception as ex:
            print(ex)
        
        return

    def CameraOutput(self):
        pic = None
        while not self.cameraStop:
            # Note: if camera is setting, do not read the camera
            if self.waitCameraSetting:
                if not self.cameraStop and pic != None:
                    self.picturebox.SetBitmap(pic)
                continue

            ret, img = self.camera.read()
            # cv2.waitKey(100)
            if ret:
                self.cameraImg = img.copy()
                pic = self.ImageConvert(self.cameraImg)
                pic = cv2.resize(pic, (850, 550))
                pic = wx.Bitmap.FromBuffer(850, 550, pic)

                # Note: Since the frame will destroy first, so use flag:cameraStop to prevent exception
                if not self.cameraStop:
                    self.picturebox.SetBitmap(pic)
            else:
                if not self.cameraStop and pic != None:
                    self.picturebox.SetBitmap(pic)
        
        self.camera.release()

    def ImageConvert(self, img):
        if not self.picHSV:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            ret = self.dialog.GetHSVValue()
            mask = cv2.inRange(hsv_img, (ret[0], ret[2], ret[4]), (ret[1], ret[3], ret[5]))
            img = cv2.bitwise_and(rgb_img,rgb_img, mask= mask)
        
        return img
    
    def BGR2RGB(self, src):
        (B,G,R) = cv2.split(src)
        img = cv2.merge([R,G,B])
        return img
    
    # Note: set camera to waiting for set parameter finish.
    def WaitCameraSettingState(self, state:bool):
        self.waitCameraSetting = state
    
    def SetPicHSVState(self, state:bool):      
        self.picHSV = state
    
    

# if __name__ == '__main__':
#     # When this module is run (not imported) then create the app, the
#     # frame, show it, and start the event loop.
#     app = wx.App()
    

#     frm = EDIUplaod(None)
    
#     app.MainLoop()