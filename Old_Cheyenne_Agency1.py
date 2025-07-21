## Workflow for the Old Cheyenne Agency
 
# set up environment (check assignment from Elsa – you might already have an environment to use there)
conda create -n lidar_env python=3.9 geopandas rasterio rioxarray xarray matplotlib contextily elevation folium pyproj
conda activate lidar_env
 
# add
pip install laspy pdal ipywidgets notebook nbconvert
 
# Download and Prepare Data
import rioxarray as rxr
import matplotlib.pyplot as plt
import numpy as np
import holoviews as hv
hv.extension('bokeh')   
import laspy
print("Available backends:", laspy.LazBackend.detect_available())

# List of file paths
filepaths = [
    "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ396985.laz",
    "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ397986.laz",
    "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ397985.laz",
    "USGS_LPC_SD_FY17_NRCS_Lidar_QSI_2017_D17_14TLQ396986.laz"
]

# Lists to store coordinate arrays
x_all, y_all, z_all = [], [], []

# Use a loop to read and store all coordinates
for path in filepaths:
    las = laspy.read(path)
    x_all.append(las.x)
    y_all.append(las.y)
    z_all.append(las.z)

# Concatenate into full arrays
x = np.concatenate(x_all)
y = np.concatenate(y_all)
z = np.concatenate(z_all)

print(f"Loaded {len(x)} total points from {len(filepaths)} tiles.")

# output: Loaded 8135293 total points from 4 tiles.

# Used a loop instead of repeating `laspy.read()` four times.
# Removed code repetition by appending data to lists and concatenating once.
# Plan to add classification

plt.figure(figsize=(10, 8))
plt.scatter(x, y, c=z, cmap='terrain', s=0.5)
plt.colorbar(label='Elevation (Z)')
plt.title("Combined LiDAR Points from four Tiles")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()


print("X range:", x.min(), "-", x.max())
print("Y range:", y.min(), "-", y.max())

# Combine coordinates and classifications
x = np.concatenate([las1.x, las2.x, las3.x, las4.x])
y = np.concatenate([las1.y, las2.y, las3.y, las4.y])
z = np.concatenate([las1.z, las2.z, las3.z, las4.z])
classification = np.concatenate([las1.classification, las2.classification, las3.classification, las4.classification])


classes, counts = np.unique(classification, return_counts=True)
print("Classification codes and counts:")
for cls, cnt in zip(classes, counts):
    print(f"Class {cls}: {cnt} points")

# Create water mask
water_mask = classification == 9

# Set up side-by-side plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), sharex=True, sharey=True)

# Full LiDAR plot
sc1 = ax1.scatter(x, y, c=z, cmap="terrain", s=1)
ax1.set_title("All LiDAR Points")
ax1.set_xlabel("X")
ax1.set_ylabel("Y")
plt.colorbar(sc1, ax=ax1, label="Elevation (Z)")

# Water-only plot
sc2 = ax2.scatter(x[water_mask], y[water_mask], c=z[water_mask], cmap="Blues", s=1)
ax2.set_title("Water-Classified Points (Class 9)")
ax2.set_xlabel("X")
plt.colorbar(sc2, ax=ax2, label="Elevation (Z)")

plt.suptitle("LiDAR Point Cloud vs Water-Classified Points", fontsize=16)
plt.tight_layout()
plt.show()

## Make sure to save/plot intermediate steps (maps, visualizations, etc.) for your project report (not added here but should be)