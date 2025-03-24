from enum import Enum

class DefaultParameter(Enum):
    Brightness = 128
    Contrast = 16
    Hue = 0.0
    Saturation = 24
    Sharpness = 8
    Whitebalance = 5000
    Autowhitebalance = 0
    Backlight = 0
    FPS = 0
    Exposure = -6
    Autoexposure = 1
    Outputwidth = 640
    Outputheight = 480
    SetHSV = 0
    HSV_H_Lower = 0
    HSV_H_Higher = 180
    HSV_S_Lower = 0
    HSV_S_Higher = 255
    HSV_V_Lower = 0
    HSV_V_Higher = 255

class CurrentParameter:

    currentParamDict = {"Brightness":DefaultParameter.Brightness.value,
                        "Contrast":DefaultParameter.Contrast.value,
                        "Hue": DefaultParameter.Hue.value,
                        "Saturation" : DefaultParameter.Saturation.value,
                        "Sharpness" : DefaultParameter.Sharpness.value,
                        "Whitebalance" :DefaultParameter.Whitebalance.value,
                        "AutoWB" : DefaultParameter.Autowhitebalance.value,
                        "BackLight" : DefaultParameter.Backlight.value,
                        "FPS": DefaultParameter.FPS.value,
                        "Exposure" : DefaultParameter.Exposure.value,
                        "Width" : DefaultParameter.Outputwidth.value,
                        "Height" : DefaultParameter.Outputheight.value,
                        "AutoExposure" : DefaultParameter.Autoexposure.value,
                        "SetHSV" : DefaultParameter.SetHSV.value,
                        "HSV_H_Lower" : DefaultParameter.HSV_H_Lower.value,
                        "HSV_H_Higher" : DefaultParameter.HSV_H_Higher.value,
                        "HSV_S_Lower" : DefaultParameter.HSV_S_Lower.value,
                        "HSV_S_Higher" : DefaultParameter.HSV_S_Higher.value,
                        "HSV_V_Lower" : DefaultParameter.HSV_V_Lower.value,
                        "HSV_V_Higher" : DefaultParameter.HSV_V_Higher.value
                        }
    
    def GetCurrentParam(self, parameter):
        return self.currentParamDict[parameter]

    def SetCurrentParam(self, parameter, value):
        self.currentParamDict[parameter] = value