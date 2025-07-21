## Workflow for the Old Cheyenne Agency
## Not in this yet but important!
##  Make sure all data is projected in the same CRS first (e.g., EPSG:32614).
##  Resample or reproject data before stacking or comparing.
 
# set up environment (check assignment from Elsa – you might already have an environment to use there)
conda create -n lidar_env python=3.9 geopandas rasterio rioxarray xarray matplotlib contextily elevation folium pyproj
conda activate lidar_env
 
# could also add
pip install laspy pdal ipywidgets notebook nbconvert
 
# Download and Prepare Data
import rioxarray as rxr
import matplotlib.pyplot as plt
 
# Load DEM
dem = rxr.open_rasterio("path/to/dem.tif", masked=True).squeeze()
 
# Plot DEM
dem.plot(cmap="terrain", figsize=(10, 6))
plt.title("Digital Elevation Model (DEM)")
plt.show()
 
# Load and Georeference Historical Maps
# historical maps should be manually georeferenced in QGIS or Arc and saved as a GeoTIFF before this step.

# Load georeferenced historical map
historic_map = rxr.open_rasterio("path/to/historic_map_georef.tif", masked=True).squeeze()
 
# Plot
historic_map.plot(figsize=(10, 6))
plt.title("Georeferenced Historical Map")
plt.show()
 
# Overlay Historical Map and DEM
fig, ax = plt.subplots(figsize=(12, 8))
dem.plot(ax=ax, cmap="terrain", alpha=0.6)
historic_map.plot(ax=ax, alpha=0.4)
plt.title("Overlay of DEM and Historical Map")
plt.show()
 
4. Analyze Lidar / Elevation Data
# create hillshade
import numpy as np
 
x, y = np.gradient(dem)
slope = np.sqrt(x**2 + y**2)
aspect = np.arctan2(-x, y)
azimuth = 315  # Light angle from NW
altitude = 45
hillshade = np.sin(np.radians(altitude)) * np.cos(slope) + \
            np.cos(np.radians(altitude)) * np.sin(slope) * np.cos(np.radians(azimuth) - aspect)
 
plt.imshow(hillshade, cmap="gray", extent=dem.rio.bounds())
plt.title("Hillshade")
plt.show()

# create Local Relief Model (for detecting archaeological features)
 # Rolling mean to smooth DEM
smoothed_dem = dem.rolling(x=5, center=True).mean().rolling(y=5, center=True).mean()
local_relief = dem - smoothed_dem
 
local_relief.plot(cmap="coolwarm", figsize=(10, 6))
plt.title("Local Relief Model")
plt.show()
 
# Overlay Historical Features
import geopandas as gpd
historical_points = gpd.read_file("path/to/old_cheyenne_features.geojson")
 
# Plot on DEM
ax = dem.plot.imshow(cmap="terrain", figsize=(12, 8))
historical_points.plot(ax=ax, color="red", markersize=10)
plt.title("Historical Features Overlay")
plt.show()
 
# Create Interactive Map
import folium 
# Adjust to match DEM extent
m = folium.Map(location=[44.5, -100], zoom_start=10) #put your actual coordinates
bounds = [[dem.rio.bounds()[1], dem.rio.bounds()[0]], [dem.rio.bounds()[3], dem.rio.bounds()[2]]]
folium.raster_layers.ImageOverlay(
    image=dem.values,
    bounds=bounds,
    opacity=0.6
).add_to(m)
 
# Add markers
for i, row in historical_points.iterrows():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row.get("name", "")).add_to(m)
 
m.save("interactive_map.html")
 
# Cross-Section Analysis (Elevation Profile)
# This is a placeholder; requires interpolation or raster sampling code and I’m not sure if you want to do this or not
transect_coords = [(44.5, -100.5), (44.6, -100.4)]
 
# Interpolate DEM values along the transect line (implement later if wanted)
 (WIP)

# Plot
elevation_values = [500, 520, 530, 525, 510]  # Replace with real values
plt.plot(elevation_values)
plt.title("Elevation Profile")
plt.xlabel("Distance along transect")
plt.ylabel("Elevation (m)")
plt.show()
 
# Analyze Raw Lidar (.las/.laz) Data
import laspy
import numpy as np
 
las = laspy.read("path/to/lidar_data.laz") # put actual path
points = np.vstack((las.x, las.y, las.z)).T
 
# Filter ground points
ground_points = points[las.classification == 2]
 
# Advanced Lidar processing can be done with PDAL (like GDAL but for point clouds) – check with Elsa
(create pdal pipeline if want to use)
 
# Elevation Pattern Detection with image segmentation (more advanced)
from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage.color import label2rgb
from sklearn.cluster import KMeans
 
def detect_elevation_patterns(elevation_data, n_clusters=3):
    elevation_gradient = sobel(elevation_data)
 
    markers = np.zeros_like(elevation_data, dtype=int)
    markers[elevation_data < np.percentile(elevation_data, 10)] = 1
    markers[elevation_data > np.percentile(elevation_data, 90)] = 2
 
    segmented_image = watershed(elevation_gradient, markers)
 
    flat_data = elevation_data.flatten().reshape(-1, 1)
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_labels = kmeans.fit_predict(flat_data)
    clustered_image = kmeans_labels.reshape(elevation_data.shape)
 
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    axes[0].imshow(elevation_data, cmap='terrain')
    axes[0].set_title("Original Elevation Data")
    axes[1].imshow(label2rgb(segmented_image, image=elevation_data, bg_label=0))
    axes[1].set_title("Watershed Segmentation")
    axes[2].imshow(clustered_image, cmap='nipy_spectral')
    axes[2].set_title("K-Means Clustering")
    plt.tight_layout()
    plt.show()
 
    return segmented_image, clustered_image

## Make sure to save/plot intermediate steps (maps, visualizations, etc.) for your project report (not added here but should be)
