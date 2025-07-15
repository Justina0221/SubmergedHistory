# SubmergedHistory
Submerged History: Remembering the Old Cheyenne Agency

## Project description: 
The Old Cheyenne Agency was a significant cultural and administrative center for the Cheyenne River Sioux Tribe, 
but it was flooded and its precise location under the Missouri River is now uncertain. Its loss reflects a broader 
erasure of Indigenous heritage due to large-scale infrastructure projects. There is currently limited public knowledge 
or access to its physical history. Understanding and acknowledging submerged Indigenous sites is crucial for historical accuracy, 
cultural preservation, and reconciliation.

![Alt text](OldMaps/oldagncy.png)

### Data description
The Datasets downloaded from the USGS site. Working with LiDAR data and Raster data. 

**LiDAR data (.laz)**
Description: High-resolution elevation raster for the region flooded for the Missouri River.

#### Instructions for Workflow
> For Python and Jupyter setup


**Setup Python environment**
Import all necessary libraries:

`import laspy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from scipy.interpolate import griddata
import numpy.ma as ma`

**Load and Combine LiDAR data**
File paths
`cheyenne_agency1 = "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ396985.laz"
 cheyenne_agency2 = "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ397986.laz"
 cheyenne_agency3 = "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ397985.laz"
 cheyenne_agency4 = "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ396986.laz"`

Read files one at a time
`las1 = laspy.read(cheyenne_agency1)
las2 = laspy.read(cheyenne_agency2)
las3 = laspy.read(cheyenne_agency3)
las4 = laspy.read(cheyenne_agency4)`

Combine x, y, z coordinates
`x = np.concatenate([las1.x, las2.x, las3.x, las4.x])
y = np.concatenate([las1.y, las2.y, las3.y, las4.y])
z = np.concatenate([las1.z, las2.z, las3.z, las4.z])`

`print(f"Loaded {len(x)} total points from both tiles")`



##### Citations
USGS LiDAR Data
Historical Maps 
