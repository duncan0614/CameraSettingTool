from CameraParameter import DefaultParameter as Parameter
from CustomizedSlider import RangeSlider
import wx, cv2, re, os
from datetime import datetime

class ParameterPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent, settingDialog):
        """"""
        wx.Panel.__init__(self, parent=parent)
        self.settingDialog = settingDialog
        self.MainFrame = settingDialog.parent
        self.camera = self.MainFrame.camera
        self.WaitCameraSettingState = self.MainFrame.WaitCameraSettingState

        girdsizer = wx.GridBagSizer(5,5)
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        border = 5
        
        # Note: Add Label
        BrightLabel = wx.StaticText(self, label="Brightness")
        BrightLabel.SetFont(font)
        girdsizer.Add(BrightLabel, (0,0), (1,1), wx.ALL, border)

        ContrastLabel = wx.StaticText(self, label="Contrast")
        ContrastLabel.SetFont(font)
        girdsizer.Add(ContrastLabel, (1,0), (1,1), wx.ALL, border)
        
        HueLabel = wx.StaticText(self, label="Hue")
        HueLabel.SetFont(font)
        girdsizer.Add(HueLabel, (2,0), (1,1), wx.ALL, border)
        
        SaturationLabel = wx.StaticText(self, label="Saturation")
        SaturationLabel.SetFont(font)
        girdsizer.Add(SaturationLabel, (3,0), (1,1), wx.ALL, border)

        SharpnessLabel = wx.StaticText(self, label="Sharpness")
        SharpnessLabel.SetFont(font)
        girdsizer.Add(SharpnessLabel, (4,0), (1,1), wx.ALL, border)

        WhiteBalanceLabel = wx.StaticText(self, label="WhiteBalance")
        WhiteBalanceLabel.SetFont(font)
        girdsizer.Add(WhiteBalanceLabel, (5,0), (1,1), wx.ALL, border)

        BackLightLabel = wx.StaticText(self, label="BackLight")
        BackLightLabel.SetFont(font)
        girdsizer.Add(BackLightLabel, (6,0), (1,1), wx.ALL, border)

        FPSLabel = wx.StaticText(self, label="FPS")
        FPSLabel.SetFont(font)
        girdsizer.Add(FPSLabel, (7,0), (1,1), wx.ALL, border)
    
        # Note: Add slider
        self.BrightnessSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Brightness"), minValue = 0, maxValue = 255, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        girdsizer.Add(self.BrightnessSld, (0,1), (1,2), wx.ALL, border)
        self.BrightnessSld.Bind(wx.EVT_SLIDER, self.SetBrightness)

        self.ContrastSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Contrast"), minValue = 0, maxValue = 63, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        girdsizer.Add(self.ContrastSld, (1,1), (1,2), wx.ALL, border)
        self.ContrastSld.Bind(wx.EVT_SLIDER, self.SetContrast)

        self.HueSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Hue"), minValue = -180, maxValue = 180, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        girdsizer.Add(self.HueSld, (2,1), (1,2), wx.ALL, border)
        self.HueSld.Bind(wx.EVT_SLIDER, self.SetHue)

        self.SaturationSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Saturation"), minValue = 0, maxValue = 63, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        girdsizer.Add(self.SaturationSld, (3,1), (1,2), wx.ALL, border)
        self.SaturationSld.Bind(wx.EVT_SLIDER, self.SetSaturation)

        self.SharpnessSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Sharpness"), minValue = 0, maxValue = 31, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        girdsizer.Add(self.SharpnessSld, (4,1), (1,2), wx.ALL, border)
        self.SharpnessSld.Bind(wx.EVT_SLIDER, self.SetSharpness)

        self.WhiteBalanceSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Whitebalance"), minValue = 1000, maxValue = 10000, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        self.WhiteBalanceSld.Enable(False)
        girdsizer.Add(self.WhiteBalanceSld, (5,1), (1,2), wx.ALL, border)
        self.WhiteBalanceSld.Bind(wx.EVT_SLIDER, self.SetWhiteBalance)

        self.BackLightSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("BackLight"), minValue = 0, maxValue = 100, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        self.BackLightSld.Enable(False)
        girdsizer.Add(self.BackLightSld, (6,1), (1,2), wx.ALL, border)
        self.BackLightSld.Bind(wx.EVT_SLIDER, self.SetBackLight)
        
        # Note: Add combo box for FPS
        self.fpscombobox = wx.ComboBox(self, choices=['0','30','60'], size=(75, 40), style=wx.CB_READONLY)
        value = str(int(self.MainFrame.currentParameter.GetCurrentParam("FPS")))
        self.fpscombobox.SetValue(value)
        girdsizer.Add(self.fpscombobox, (7,1), (1,1), wx.ALL, border)
        self.fpscombobox.Bind(wx.EVT_COMBOBOX, self.SetFPS)

        # Note: Add Defalt button
        self.defaultbtn = wx.Button(self, size=(75, 40))
        self.defaultbtn.SetLabel("Default")
        self.defaultbtn.SetFont(font)
        girdsizer.Add(self.defaultbtn, (8,1), (1,1), wx.ALL, border)
        self.defaultbtn.Bind(wx.EVT_BUTTON, self.SetDefaultParameter)
        
        # Note: Add checkbox for auto white balance
        self.autoCheckbox = wx.CheckBox(self, label = 'Auto',pos = (10,10))
        self.autoCheckbox.SetFont(font)
        self.autoCheckbox.SetValue(self.MainFrame.currentParameter.GetCurrentParam("AutoWB"))
        self.autoCheckbox.Enable(False)
        girdsizer.Add(self.autoCheckbox, (5,3), (1,1), wx.ALL, border)
        self.autoCheckbox.Bind(wx.EVT_CHECKBOX, self.SetAutoWhiteBalance)

        self.SetSizer(girdsizer)

    # Note: Events for the sliders
    def SetBrightness(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.BrightnessSld.GetValue()
        self.camera.set(cv2.CAP_PROP_BRIGHTNESS, float(value))
        self.WaitCameraSettingState(False)

    def SetContrast(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.ContrastSld.GetValue()
        self.camera.set(cv2.CAP_PROP_CONTRAST, float(value))
        self.WaitCameraSettingState(False)

    def SetHue(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.HueSld.GetValue()
        self.camera.set(cv2.CAP_PROP_HUE, float(value))
        self.WaitCameraSettingState(False)

    def SetSaturation(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.SaturationSld.GetValue()
        self.camera.set(cv2.CAP_PROP_SATURATION, float(value))
        self.WaitCameraSettingState(False)
    
    def SetSharpness(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.SharpnessSld.GetValue()
        self.camera.set(cv2.CAP_PROP_SHARPNESS, float(value))
        self.WaitCameraSettingState(False)

    def SetWhiteBalance(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.WhiteBalanceSld.GetValue()
        self.camera.set(cv2.CAP_PROP_WB_TEMPERATURE, float(value))
        self.WaitCameraSettingState(False)
    
    def SetBackLight(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.BackLightSld.GetValue()
        self.camera.set(cv2.CAP_PROP_BACKLIGHT, float(value))
        self.WaitCameraSettingState(False)
    
    # Note: Event for combobox
    def SetFPS(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = self.fpscombobox.GetValue()
        self.camera.set(cv2.CAP_PROP_FPS, float(value))
        self.WaitCameraSettingState(False)

    # Note: Event for checkbox
    def SetAutoWhiteBalance(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        value = event.IsChecked()
        if value:
            self.camera.set(cv2.CAP_PROP_AUTO_WB, 1)
            self.WhiteBalanceSld.Enable(False)
        else:
            self.camera.set(cv2.CAP_PROP_AUTO_WB, 0)
            self.WhiteBalanceSld.Enable(True)
        self.WaitCameraSettingState(False)
    
    # Note: Event for button
    def SetDefaultParameter(self, event):
        self.settingDialog.SetParameterApply(False)
        self.WaitCameraSettingState(True)
        self.camera.set(cv2.CAP_PROP_BRIGHTNESS, float(Parameter.Brightness.value))
        self.camera.set(cv2.CAP_PROP_CONTRAST, float(Parameter.Contrast.value))
        self.camera.set(cv2.CAP_PROP_HUE, float(Parameter.Hue.value))
        self.camera.set(cv2.CAP_PROP_SATURATION, float(Parameter.Saturation.value))
        self.camera.set(cv2.CAP_PROP_SHARPNESS, float(Parameter.Sharpness.value))
        self.camera.set(cv2.CAP_PROP_WB_TEMPERATURE, float(Parameter.Whitebalance.value))
        self.camera.set(cv2.CAP_PROP_BACKLIGHT, float(Parameter.Backlight.value))
        self.camera.set(cv2.CAP_PROP_FPS, float(Parameter.FPS.value))
        self.camera.set(cv2.CAP_PROP_AUTO_WB, int(Parameter.Autowhitebalance.value))

        self.BrightnessSld.SetValue(float(Parameter.Brightness.value))
        self.ContrastSld.SetValue(float(Parameter.Contrast.value))
        self.HueSld.SetValue(float(Parameter.Hue.value))
        self.SaturationSld.SetValue(float(Parameter.Saturation.value))
        self.SharpnessSld.SetValue(float(Parameter.Sharpness.value))
        self.WhiteBalanceSld.SetValue(float(Parameter.Whitebalance.value))
        self.BackLightSld.SetValue(float(Parameter.Backlight.value))
        self.fpscombobox.SetValue(str(Parameter.FPS.value))
        self.autoCheckbox.SetValue(int(Parameter.Autowhitebalance.value))
        self.WaitCameraSettingState(False)

class ControlPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent, settingDialog):
        """"""
        wx.Panel.__init__(self, parent=parent)
        self.settingDialog = settingDialog
        self.MainFrame = settingDialog.parent
        self.camera = self.MainFrame.camera
        self.WaitCameraSettingState = self.MainFrame.WaitCameraSettingState
        self.SetPicHSVState = self.MainFrame.SetPicHSVState

        girdsizer = wx.GridBagSizer(5,5)
        font12 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        font14 = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        border = 5

        # Note: Add Label
        ExposureLabel = wx.StaticText(self, label="Exposure")
        ExposureLabel.SetFont(font14)
        girdsizer.Add(ExposureLabel, (0,0), (1,1), wx.ALL, border)

        OutputLabel = wx.StaticText(self, label="Output")
        OutputLabel.SetFont(font14)
        girdsizer.Add(OutputLabel, (1,0), (1,1), wx.ALL, border)

        H_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        S_hsizer = wx.BoxSizer(wx.HORIZONTAL)
        V_hsizer = wx.BoxSizer(wx.HORIZONTAL)

        HLabel = wx.StaticText(self, label="H:")
        HLabel.SetFont(font14)
        H_hsizer.Add(HLabel, flag = wx.ALL, border = 5)

        SLabel = wx.StaticText(self, label="S:")
        SLabel.SetFont(font14)
        S_hsizer.Add(SLabel, flag = wx.ALL, border = 5)

        VLabel = wx.StaticText(self, label="V:")
        VLabel.SetFont(font14)
        V_hsizer.Add(VLabel, flag = wx.ALL, border = 5)
        
        self.H_rangesLabel = wx.StaticText(self)
        self.H_rangesLabel.SetFont(font12)
        girdsizer.Add(self.H_rangesLabel, (4,1), (1,1), wx.ALL, border)

        self.S_rangesLabel = wx.StaticText(self)
        self.S_rangesLabel.SetFont(font12)
        girdsizer.Add(self.S_rangesLabel, (6,1), (1,1), wx.ALL, border)

        self.V_rangesLabel = wx.StaticText(self)
        self.V_rangesLabel.SetFont(font12)
        girdsizer.Add(self.V_rangesLabel, (8,1), (1,1), wx.ALL, border)

        # Note: Add slider
        expsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ExposureSld = wx.Slider(self, value = self.MainFrame.currentParameter.GetCurrentParam("Exposure"), minValue = -13, maxValue = 0, style = wx.SL_HORIZONTAL|wx.SL_LABELS, size = (270, 40))
        self.ExposureSld.Bind(wx.EVT_SLIDER, self.SetExposure)
        if self.MainFrame.currentParameter.GetCurrentParam("AutoExposure") == 1:
            self.ExposureSld.Enable(False)
        else:
            self.ExposureSld.Enable(True)

        self.H_rangeslider = RangeSlider(parent=self, lowValue=0, highValue=180, minValue=0, maxValue=180, size = (420, 20))
        H_hsizer.Add(self.H_rangeslider, wx.ALL, border)
        girdsizer.Add(H_hsizer, (3,0), (1,3), wx.ALL, border)
        self.H_rangeslider.Bind(wx.EVT_SLIDER, self.H_rangeslider_changed)
        self.H_rangeslider.SetValues(self.MainFrame.currentParameter.GetCurrentParam("HSV_H_Lower"), self.MainFrame.currentParameter.GetCurrentParam("HSV_H_Higher"))      

        self.S_rangeslider = RangeSlider(parent=self, lowValue=0, highValue=255, minValue=0, maxValue=255, size = (420, 20))
        S_hsizer.Add(self.S_rangeslider, wx.ALL, border)
        girdsizer.Add(S_hsizer, (5,0), (1,3), wx.ALL, border)
        self.S_rangeslider.Bind(wx.EVT_SLIDER, self.S_rangeslider_changed)
        self.S_rangeslider.SetValues(self.MainFrame.currentParameter.GetCurrentParam("HSV_S_Lower"), self.MainFrame.currentParameter.GetCurrentParam("HSV_S_Higher"))

        self.V_rangeslider = RangeSlider(parent=self, lowValue=0, highValue=255, minValue=0, maxValue=255, size = (420, 20))
        V_hsizer.Add(self.V_rangeslider, wx.ALL, border)
        girdsizer.Add(V_hsizer, (7,0), (1,3), wx.ALL, border)
        self.V_rangeslider.Bind(wx.EVT_SLIDER, self.V_rangeslider_changed)
        self.V_rangeslider.SetValues(self.MainFrame.currentParameter.GetCurrentParam("HSV_V_Lower"), self.MainFrame.currentParameter.GetCurrentParam("HSV_V_Higher"))

        # Note: Add combo box for Output
        self.outputcombobox = wx.ComboBox(self, choices=['1920 * 1080', '1280 * 720','640 * 480', '640 *360'], size=(100, 40), style=wx.CB_READONLY)
        self.outputcombobox.SetSelection(2)
        # self.outputcombobox.Enable(False)
        girdsizer.Add(self.outputcombobox, (1,1), (1,1), wx.ALL, border)
        self.outputcombobox.Bind(wx.EVT_COMBOBOX, self.SetOutput)

        # Note: Add checkbox
        self.autoexpcheckbox = wx.CheckBox(self, label = 'Auto',pos = (20,20))
        self.autoexpcheckbox.SetFont(font14)

        # Put two component into expSizer
        expsizer.Add(self.autoexpcheckbox, wx.ALL, border = 5)
        expsizer.Add(self.ExposureSld, flag = wx.ALL, border = 5)
        girdsizer.Add(expsizer, (0,1), (1,1), wx.ALL, border)
        self.autoexpcheckbox.Bind(wx.EVT_CHECKBOX, self.SetAutoExposure)
        self.autoexpcheckbox.SetValue(self.MainFrame.currentParameter.GetCurrentParam("AutoExposure"))

        self.HSVCheckbox = wx.CheckBox(self, label = 'HSV PIC',pos = (20,20))
        self.HSVCheckbox.SetFont(font14)
        girdsizer.Add(self.HSVCheckbox, (2,0), (1,1), wx.ALL, border)
        self.HSVCheckbox.Bind(wx.EVT_CHECKBOX, self.SetHSVPic)
        self.HSVCheckbox.SetValue(self.MainFrame.currentParameter.GetCurrentParam("SetHSV"))

        # self.HSVbtn = wx.Button(self, size=(90,40), label = 'HSV PIC')
        # self.HSVbtn.SetFont(font14)
        # girdsizer.Add(self.HSVbtn, (2,1), (1,1), wx.ALL|wx.ALIGN_RIGHT, border)
        # self.HSVbtn.Bind(wx.EVT_BUTTON, self.ShowHSVPic)

        if self.HSVCheckbox.IsChecked():
            self.H_rangeslider.Enable(True)
            self.S_rangeslider.Enable(True)
            self.V_rangeslider.Enable(True)
        else:
            self.H_rangeslider.Enable(False)
            self.S_rangeslider.Enable(False)
            self.V_rangeslider.Enable(False)

        # Note: Add button
        self.graybtn = wx.Button(self, size=(90,40), label = 'Gray PIC')
        self.graybtn.SetFont(font14)
        girdsizer.Add(self.graybtn, (10,0), (1,1), wx.ALL|wx.ALIGN_RIGHT, border)
        self.graybtn.Bind(wx.EVT_BUTTON, self.ShowGrayPic)

        self.defaultbtn = wx.Button(self, size=(75, 40))
        self.defaultbtn.SetLabel("Default")
        self.defaultbtn.SetFont(font14)
        girdsizer.Add(self.defaultbtn, (10,1), (1,1), wx.ALL, border)
        self.defaultbtn.Bind(wx.EVT_BUTTON, self.SetDefaultParameter)

        self.SetSizer(girdsizer)

    # Note: Events for the sliders
    def SetExposure(self, event):
        self.settingDialog.SetControlApply(False)
        self.WaitCameraSettingState(True)
        value = self.ExposureSld.GetValue()
        self.camera.set(cv2.CAP_PROP_EXPOSURE, int(value))
        self.WaitCameraSettingState(False)
    
    # Note: Event for combobox
    def SetOutput(self, event):
        self.settingDialog.SetControlApply(False)
        self.WaitCameraSettingState(True)
        value = self.outputcombobox.GetValue()
        ret = re.findall(r'\d+', value)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, float(ret[0]))
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, float(ret[1]))
        # print(self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        # print(self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.WaitCameraSettingState(False)

    # Note: Event for checkbox
    def SetAutoExposure(self, event):
        self.settingDialog.SetControlApply(False)
        self.WaitCameraSettingState(True)
        value = event.IsChecked()
        if value:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            self.ExposureSld.Enable(False)
        else:
            self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
            self.ExposureSld.Enable(True)
        self.WaitCameraSettingState(False)
    
    def SetHSVPic(self, event):
        self.settingDialog.SetControlApply(False)
        self.WaitCameraSettingState(True)
        value = event.IsChecked()
        if value:
            self.SetPicHSVState(True)
            self.H_rangeslider.Enable(True)
            self.S_rangeslider.Enable(True)
            self.V_rangeslider.Enable(True)
        else:
            self.SetPicHSVState(False)
            self.H_rangeslider.Enable(False)
            self.S_rangeslider.Enable(False)
            self.V_rangeslider.Enable(False)
        self.WaitCameraSettingState(False)
    
    # def H_convert(self, val):

    #     hLowVal = cv2.getTrackbarPos("H Low", "HSVImage")
    #     hHighVal = cv2.getTrackbarPos("H High", "HSVImage")
    #     sLowVal = cv2.getTrackbarPos("S Low", "HSVImage")
    #     sHighVal = cv2.getTrackbarPos("S High", "HSVImage")
    #     vLowVal = cv2.getTrackbarPos("V Low", "HSVImage")
    #     vHighVal = cv2.getTrackbarPos("V High", "HSVImage")
        
    #     # Let low value cannot over than high value
    #     if hLowVal > hHighVal:
    #         cv2.setTrackbarPos("H Low", "HSVImage", hHighVal)
    #         hLowVal = hHighVal
    #         cv2.setTrackbarPos("H High", "HSVImage", hLowVal)
    #         hHighVal = hLowVal
        
    #     if sLowVal > sHighVal:
    #         cv2.setTrackbarPos("H Low", "HSVImage", sHighVal)
    #         sLowVal = sHighVal
    #         cv2.setTrackbarPos("H High", "HSVImage", sLowVal)
    #         sHighVal = sLowVal

    #     if vLowVal > vHighVal:
    #         cv2.setTrackbarPos("H Low", "HSVImage", vHighVal)
    #         vLowVal = vHighVal
    #         cv2.setTrackbarPos("H High", "HSVImage", vLowVal)
    #         vHighVal = vLowVal
        
    #     mask = cv2.inRange(self.hsv_img, (hLowVal, sLowVal, vLowVal), (hHighVal, sHighVal, vHighVal))
    #     img = cv2.bitwise_and(self.rgb_img,self.rgb_img, mask= mask)
    #     cv2.imshow("HSVImage", img)

    # def ShowHSVPic(self, event):
    #     self.rgb_img = cv2.cvtColor(self.MainFrame.cameraImg, cv2.COLOR_BGR2RGB)
    #     self.hsv_img = cv2.cvtColor(self.rgb_img, cv2.COLOR_BGR2HSV)
    #     cv2.imshow("HSVImage", self.hsv_img)
    #     cv2.createTrackbar('H Low', 'HSVImage', 0, 180, self.H_convert)
    #     cv2.createTrackbar('H High', 'HSVImage', 180, 180, self.H_convert)
    #     cv2.createTrackbar('S Low', 'HSVImage', 0, 255, self.H_convert)
    #     cv2.createTrackbar('S High', 'HSVImage', 255, 255, self.H_convert)
    #     cv2.createTrackbar('V Low', 'HSVImage', 0, 255, self.H_convert)
    #     cv2.createTrackbar('V High', 'HSVImage', 255, 255, self.H_convert)
        

    def ShowGrayPic(self, event):
        img = cv2.cvtColor(self.MainFrame.cameraImg, cv2.COLOR_BGR2GRAY)
        value = self.outputcombobox.GetValue()
        ret = re.findall(r'\d+', value)
        resized_img = cv2.resize(img, (int(ret[0]), int(ret[1])))
        cv2.imshow("Gray Image", resized_img)
        nowTime = datetime.now()
        if not os.path.exists("Pictures"):
            os.mkdir("Pictures")
        cv2.imwrite(f"Pictures\\Gray_{nowTime.strftime('%Y%m%d%H%M%S')}.jpg", img)

    def H_rangeslider_changed(self, evt):
        obj = evt.GetEventObject()
        lv, hv = obj.GetValues()
        self.H_rangesLabel.SetLabel('Low value: {:.0f}, High value: {:.0f}'.format(lv, hv))

    def S_rangeslider_changed(self, evt):
        obj = evt.GetEventObject()
        lv, hv = obj.GetValues()
        self.S_rangesLabel.SetLabel('Low value: {:.0f}, High value: {:.0f}'.format(lv, hv))

    def V_rangeslider_changed(self, evt):
        obj = evt.GetEventObject()
        lv, hv = obj.GetValues()
        self.V_rangesLabel.SetLabel('Low value: {:.0f}, High value: {:.0f}'.format(lv, hv))
    
    # Note: Event for button
    def SetDefaultParameter(self, event):
        self.settingDialog.SetControlApply(False)
        self.WaitCameraSettingState(True)
        self.camera.set(cv2.CAP_PROP_EXPOSURE, int(Parameter.Exposure.value))
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, float(Parameter.Outputwidth.value))
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, float(Parameter.Outputheight.value))  
        self.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, int(Parameter.Autoexposure.value))
        self.SetPicHSVState(False)
        self.WaitCameraSettingState(False)

        self.ExposureSld.SetValue(int(Parameter.Exposure.value))
        self.autoexpcheckbox.SetValue(Parameter.Autoexposure.value)
        self.HSVCheckbox.SetValue(Parameter.SetHSV.value)

        for item in self.outputcombobox.GetItems():
            if str(Parameter.Outputwidth.value) in item and str(Parameter.Outputheight.value) in item:
                self.outputcombobox.SetValue(item)
                break        
        

class SettingDialog(wx.Dialog):

    parameterApply = False
    controlApply = False

    def __init__(self, parent):
        super(SettingDialog, self).__init__(parent, size = wx.Size(500, 640), style=wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        if parent != None:
            self.parent = parent

        self.SetTitle('Camera Setting')
        self.SetMinSize(wx.Size(500, 640))
        self.SetMaxSize(wx.Size(500, 640))

        self.InitUI()

        if self.parent.camera == None:
            self.tabOne1.Enable(False)
            self.tabOne2.Enable(False)
            self.applybtn.Enable(False)
            self.confirmbtn.Enable(False)

    def InitUI(self):

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.AddSpacer(5)
        font = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        panel = wx.Panel(self)
        
        self.notebook = wx.Notebook(panel)
        self.notebook.SetSize(490, 520)
        self.tabOne1 = ParameterPanel(self.notebook, self)
        self.notebook.AddPage(self.tabOne1, "Camera Parameter")

        self.tabOne2 = ControlPanel(self.notebook, self)
        self.notebook.AddPage(self.tabOne2, "Camera Control")

        self.notebook.SetFont(font)
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.PageChanged)
        vsizer.Add(self.notebook, 0, wx.RIGHT| wx.LEFT | wx.EXPAND, 5)

        btnStartPos = 12
        gridsizer = wx.GridBagSizer(0,7)
        self.confirmbtn = wx.Button(panel, size=(75, 40))
        self.confirmbtn.SetLabel("Confirm")
        self.confirmbtn.SetFont(font)
        gridsizer.Add(self.confirmbtn, (1,btnStartPos), (1,1), wx.ALL, 5)

        cancelbtn = wx.Button(panel, size=(75, 40))
        cancelbtn.SetLabel("Cancel")
        cancelbtn.SetFont(font)
        gridsizer.Add(cancelbtn, (1,btnStartPos+1), (1,1), wx.ALL, 5)

        self.applybtn = wx.Button(panel, size=(75, 40))
        self.applybtn.SetLabel("Apply")
        self.applybtn.SetFont(font)
        gridsizer.Add(self.applybtn, (1,btnStartPos+2), (1,1), wx.ALL, 5)
        vsizer.Add(gridsizer, 0, wx.LEFT, 8)

        panel.SetSizer(vsizer)

        self.Bind( wx.EVT_BUTTON, self.CancelClick, cancelbtn)
        self.Bind( wx.EVT_BUTTON, self.ConfirmClick, self.confirmbtn)
        self.Bind( wx.EVT_BUTTON, self.ApplyClick, self.applybtn)
        self.Centre()
    
    def PageChanged(self, event):
        value = self.notebook.GetSelection()
        if value == 0:
            if self.parameterApply:
                self.applybtn.Enable(False)
            else:
                self.applybtn.Enable(True)
        elif value == 1:
            if self.controlApply:
                self.applybtn.Enable(False)
            else:
                self.applybtn.Enable(True)
    
    def CancelClick(self, event):
        if self.parent.camera != None:
            self.SetOriginParameter()
        cv2.destroyAllWindows()
        self.Close()
    
    def ConfirmClick(self, event):
        self.SaveCurrentParameter()
        cv2.destroyAllWindows()
        self.Close()

    def ApplyClick(self, event):
        value = self.notebook.GetSelection()
        if int(value) == 0:
            self.SetParameterApply(True)
        elif int(value) == 1:
            self.SetControlApply(True)
        self.ApplyCurrentParameter()
    
    def SetParameterApply(self, state:bool):
        if state:
            self.parameterApply = True
            self.applybtn.Enable(False)
        else:
            self.parameterApply = False
            self.applybtn.Enable(True)

    def SetControlApply(self, state:bool):
        if state:
            self.controlApply = True
            self.applybtn.Enable(False)
        else:
            self.controlApply = False
            self.applybtn.Enable(True)

    def GetHSVValue(self) -> list:
        hsv_value_List = []
        for item in (self.tabOne2.H_rangeslider, self.tabOne2.S_rangeslider, self.tabOne2.V_rangeslider):
            lv, hv = item.GetValues()
            hsv_value_List.append(lv)
            hsv_value_List.append(hv)
        
        return hsv_value_List

    def SetOriginParameter(self):
        self.parent.WaitCameraSettingState(True)
        if not self.parameterApply:
            self.parent.camera.set(cv2.CAP_PROP_BRIGHTNESS, float(self.parent.currentParameter.GetCurrentParam("Brightness")))
            self.parent.camera.set(cv2.CAP_PROP_CONTRAST, float(self.parent.currentParameter.GetCurrentParam("Contrast")))
            self.parent.camera.set(cv2.CAP_PROP_HUE, float(self.parent.currentParameter.GetCurrentParam("Hue")))
            self.parent.camera.set(cv2.CAP_PROP_SATURATION, float(self.parent.currentParameter.GetCurrentParam("Saturation")))
            self.parent.camera.set(cv2.CAP_PROP_SHARPNESS, float(self.parent.currentParameter.GetCurrentParam("Sharpness")))
            self.parent.camera.set(cv2.CAP_PROP_WB_TEMPERATURE, float(self.parent.currentParameter.GetCurrentParam("Whitebalance")))
            self.parent.camera.set(cv2.CAP_PROP_BACKLIGHT, float(self.parent.currentParameter.GetCurrentParam("BackLight")))
            self.parent.camera.set(cv2.CAP_PROP_AUTO_WB, int(self.parent.currentParameter.GetCurrentParam("AutoWB")))
            self.parent.camera.set(cv2.CAP_PROP_FPS, int(self.parent.currentParameter.GetCurrentParam("FPS")))
        elif not self.controlApply:
            self.parent.camera.set(cv2.CAP_PROP_EXPOSURE, int(self.parent.currentParameter.GetCurrentParam("Exposure")))
            self.parent.camera.set(cv2.CAP_PROP_FRAME_WIDTH, float(self.parent.currentParameter.GetCurrentParam("Width")))
            self.parent.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, float(self.parent.currentParameter.GetCurrentParam("Height")))  
            self.parent.camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, int(self.parent.currentParameter.GetCurrentParam("AutoExposure")))
            self.parent.SetPicHSVState(self.parent.currentParameter.GetCurrentParam("SetHSV"))
        self.parent.WaitCameraSettingState(False)

    def SaveCurrentParameter(self):
        ret = self.tabOne1.BrightnessSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Brightness", int(ret))
        ret = self.tabOne1.ContrastSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Contrast", int(ret))
        ret = self.tabOne1.HueSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Hue", int(ret))
        ret = self.tabOne1.SaturationSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Saturation", int(ret))
        ret = self.tabOne1.SharpnessSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Sharpness", int(ret))
        ret = self.tabOne1.WhiteBalanceSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Whitebalance", int(ret))
        ret = self.tabOne1.BackLightSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("BackLight", int(ret))
        ret = self.tabOne1.autoCheckbox.GetValue()
        self.parent.currentParameter.SetCurrentParam("AutoWB", int(ret))
        ret = self.tabOne1.fpscombobox.GetValue()
        self.parent.currentParameter.SetCurrentParam("FPS", int(ret))
        ret = self.tabOne2.ExposureSld.GetValue()
        self.parent.currentParameter.SetCurrentParam("Exposure", int(ret))
        ret = self.tabOne2.outputcombobox.GetValue()
        value = re.findall(r'\d+', ret)
        self.parent.currentParameter.SetCurrentParam("Width", int(value[0]))
        self.parent.currentParameter.SetCurrentParam("Height", int(value[1]))
        ret = self.tabOne2.autoexpcheckbox.GetValue()
        self.parent.currentParameter.SetCurrentParam("AutoExposure", int(ret))
        ret = self.tabOne2.HSVCheckbox.GetValue()
        self.parent.currentParameter.SetCurrentParam("SetHSV", int(ret))
        lv, hv = self.tabOne2.H_rangeslider.GetValues()
        self.parent.currentParameter.SetCurrentParam("HSV_H_Lower", int(lv))
        self.parent.currentParameter.SetCurrentParam("HSV_H_Higher", int(hv))
        lv, hv = self.tabOne2.S_rangeslider.GetValues()
        self.parent.currentParameter.SetCurrentParam("HSV_S_Lower", int(lv))
        self.parent.currentParameter.SetCurrentParam("HSV_S_Higher", int(hv))
        lv, hv = self.tabOne2.V_rangeslider.GetValues()
        self.parent.currentParameter.SetCurrentParam("HSV_V_Lower", int(lv))
        self.parent.currentParameter.SetCurrentParam("HSV_V_Higher", int(hv))

    def ApplyCurrentParameter(self):
        if self.parameterApply:
            ret = self.tabOne1.BrightnessSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Brightness", int(ret))
            ret = self.tabOne1.ContrastSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Contrast", int(ret))
            ret = self.tabOne1.HueSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Hue", int(ret))
            ret = self.tabOne1.SaturationSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Saturation", int(ret))
            ret = self.tabOne1.SharpnessSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Sharpness", int(ret))
            ret = self.tabOne1.WhiteBalanceSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Whitebalance", int(ret))
            ret = self.tabOne1.BackLightSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("BackLight", int(ret))
            ret = self.tabOne1.autoCheckbox.GetValue()
            self.parent.currentParameter.SetCurrentParam("AutoWB", int(ret))
            ret = self.tabOne1.fpscombobox.GetValue()
            self.parent.currentParameter.SetCurrentParam("FPS", int(ret))
        elif self.controlApply:
            ret = self.tabOne2.ExposureSld.GetValue()
            self.parent.currentParameter.SetCurrentParam("Exposure", int(ret))
            ret = self.tabOne2.outputcombobox.GetValue()
            value = re.findall(r'\d+', ret)
            self.parent.currentParameter.SetCurrentParam("Width", int(value[0]))
            self.parent.currentParameter.SetCurrentParam("Height", int(value[1]))
            ret = self.tabOne2.autoexpcheckbox.GetValue()
            self.parent.currentParameter.SetCurrentParam("AutoExposure", int(ret))
            ret = self.tabOne2.HSVCheckbox.GetValue()
            self.parent.currentParameter.SetCurrentParam("SetHSV", int(ret))
            lv, hv = self.tabOne2.H_rangeslider.GetValues()
            self.parent.currentParameter.SetCurrentParam("HSV_H_Lower", int(lv))
            self.parent.currentParameter.SetCurrentParam("HSV_H_Higher", int(hv))
            lv, hv = self.tabOne2.S_rangeslider.GetValues()
            self.parent.currentParameter.SetCurrentParam("HSV_S_Lower", int(lv))
            self.parent.currentParameter.SetCurrentParam("HSV_S_Higher", int(hv))
            lv, hv = self.tabOne2.V_rangeslider.GetValues()
            self.parent.currentParameter.SetCurrentParam("HSV_V_Lower", int(lv))
            self.parent.currentParameter.SetCurrentParam("HSV_V_Higher", int(hv))

if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    dialog = SettingDialog(None)
    dialog.ShowModal()
    if dialog.stationSelected == False:
        wx.MessageBox("close station")
    dialog.Destroy()
    app.MainLoop()