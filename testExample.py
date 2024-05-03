# import liteBox as lb
from liteBox import detCal

#create litebox detCal object to store difcal data 
detcal = detCal()

#load lite difcal into object
detcal.loadh5("diffract_consts_058885_v0003.h5")

#check its status
print(f"detcal is native: {detcal.isNative}")

#convert from lite to native
print(("converting..."))
detcal.makeNative()

#check new status
print(f"detcal is native: {detcal.isNative}")

#save output difcal file
detcal.saveh5("native.h5")
