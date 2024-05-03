# convert lite difcal .h5 to non-lite .h5
import h5py
import numpy as np
import shutil
import time
import os
print('h5py version:',h5py.__version__)


class detCal:

    '''detCal is a class to hold calibration information (either Lite or Native)'''

    def __init__(self):

        self.detID=np.array([])
        self.difc=np.array([])
        self.difa=np.array([])
        self.zero=np.array([])
        self.group=np.array([])
        self.instSource=np.array([])
        self.instName=np.array([])
        self.mask=np.array([])
        self.inputFilename=''
        self.isNative = True
        self.nPixels = 1179648

    def loadh5(self,inputFilename):

        '''loadLite is a method to poplulate detCal with'''

        time_0 = time.time()
        
        # #create output directory if it doesn't exist
        # if not os.path.exists(os.path.dirname(outFileName)):
        #   os.mkdir(os.path.dirname(outFileName))

        # fSize = os.path.getsize(LiteFileName)
        # print(f'  Copying original .nxs.h5 file: {LiteFileName} size: {fSize/1e9:.4f} Gb')

        #TODO: check file exists and pass error if it doesn't

        self.inputFilename = inputFilename

        #open and load lite file.
        h5obj = h5py.File(self.inputFilename,'r')
        self.detID = np.array(h5obj["calibration/detid"])
        self.difc = np.array(h5obj["calibration/difc"])
        self.group=np.array(h5obj["calibration/group"])
        self.instSource = str(h5obj["calibration/instrument/instrument_source"][0],encoding='ascii')
        self.instName = str(h5obj["calibration/instrument/name"][0],encoding='ascii')
        self.mask = np.array(h5obj["calibration/use"])

        #these arrays may not be present
        try:
            self.difa = np.array(h5obj["calibration/difa"])
        except Exception:
            pass
        try:
            self.zero = np.array(h5obj["calibration/zero"])
        except Exception:
            pass

        print(f"loaded input: {self.inputFilename}")
        # print(f"   - found {len(self.detID)} DIFC values")

        if len(self.detID) == 18432:
            self.isNative=False
            self.nPixels = 18432
            print("This file is Lite")
        elif len(self.detID) == 1179648:
            self.isNative=True
            self.nPixels = 1179648
            print("This file is Native")
        return
    
    def saveh5(self,outputFilename):
        
        self.outputFilename=outputFilename
        f = h5py.File(outputFilename,'w')
        f['calibration/detid']=self.detID
        if np.any(self.difa):
            f['calibration/difa']=self.difa
        f['calibration/difc']=self.difc
        
        if np.any(self.zero):
            f['calibration/zero']=self.zero
        f['calibration/group']=self.group
        
        f['calibration/instrument/instrument_source'] = self.instSource
        f['calibration/instrument/name'] = self.instName
        f['calibration/use']=self.mask
        f.close()

    def makeNative(self):
        ''' converts a lite detcal to a native detcal '''
        
        if self.isNative:
            print('input is already native')
            return
        
        self.isNative = True
        self.detID = np.array(range(1179648))
        self.difc = self._lite2NativeArray(self.difc)
        self.group = self._lite2NativeArray(self.group)
        self.mask = self._lite2NativeArray(self.mask)

        if np.any(self.difa):
            self.difa = self._lite2NativeArray(self.difa)

        if np.any(self.zero):
            self.zero = self._lite2NativeArray(self.zero)

        self.instName='SNAP'
        self.instName='SNAP_Definition.xml' #TODO: get xml string
    
    def _lite2NativeArray(self,liteIn):
        # returns a native resolution version of an numpy array

        nativeID = np.array(range(1179648))
        Nx = 256 #native number of horizontal pixels 
        Ny = 256 #native number of vertical pixels 
        NNat = Nx*Ny #native number of pixels per panel

        #lite dimensions
        xdim = 8
        ydim = 8

        firstPix = (nativeID // NNat)*NNat
        redID = nativeID % NNat #reduced ID beginning at zero in each panel

        (i,j) = divmod(redID,Ny) #native (reduced) coordinates on pixel face
        # print(f"i is size {len(i)}, j is size {len(j)}")

        superi = divmod(i,xdim)[0]
        superj = divmod(j,ydim)[0]

        #super panel   
        superNx = Nx/xdim #32 running from 0 to 31
        superNy = Ny/ydim
        superN = superNx*superNy

        superFirstPix = (firstPix/NNat)*superN

        super = superi*superNy+superj+superFirstPix
        super = super.astype('int')

        nativeOut = liteIn[super[nativeID]]

        return nativeOut