# Overview

Data measured on the SNAP neutron diffractometer at the Spallation Neutron Source consist of a set of arrays containing neutron events. Each event is assigned an ID that identifies the detector pixel the corresponding neutron was measured in. At native resolution, the instrument has 1,179,648 pixels. 

For some datasets, it is useful to downsample this resolution by relabelling events such that 8x8 array of native pixels is given a single ID. The resultant "virtual" instrument has 18,432 pixels and the corresponding data set is termed "Lite". When compressed, Lite data can be substantially smaller than Native data and operations that depend on iterative passes through the pixels are 64 times faster.

The python module `liteBox` supports some transformations between Lite and Native resolution data.

# Current functionality

Currently, the only existing functionality is to support conversion of a `.h5` format "difcal" file from Lite to Native.

# Instructions

1. clone the repo
2. inspect, edit and run the included python script testExample.py

# Contact

m.guthrie@ornl.gov
