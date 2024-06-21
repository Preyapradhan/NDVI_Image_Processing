import rasterio
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plotting
import matplotlib.pyplot as plt
import geopandas as gpd

def compute_ndvi(B4_path, B5_path, output_path):
    with rasterio.open(B4_path) as B4, rasterio.open(B5_path) as B5:
        B4_Data = B4.read(1).astype(np.float32)
        B5_Data = B5.read(1).astype(np.float32)
        
        ndvi = (B5_Data - B4_Data) / (B5_Data + B4_Data)
        ndvi[np.isinf(ndvi)] = np.nan

        profile = B4.profile
        profile.update(dtype=rasterio.float32, count=1, nodata=np.nan)
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(ndvi, 1)

def plot_ndvi(ndvi_image, extent_array, vmin, cmap, output_image):
    with rasterio.open(ndvi_image) as src:
        ndvi = src.read(1)
    
    plt.figure(figsize=(8, 8))
    im = plt.imshow(ndvi, vmin=vmin, cmap=cmap, extent=extent_array)
    plt.colorbar(im, fraction=0.015)
    plt.xlabel('East')
    plt.ylabel('North')
    plt.savefig(output_image, bbox_inches='tight')
    plt.close()

def process_ndvi_change(B4_path_1, B5_path_1, B4_path_2, B5_path_2, ndvi_path_1, ndvi_path_2, ndvi_change_path, ndvi_change_image):
    compute_ndvi(B4_path_1, B5_path_1, ndvi_path_1)
    compute_ndvi(B4_path_2, B5_path_2, ndvi_path_2)
    
    with rasterio.open(ndvi_path_1) as src1, rasterio.open(ndvi_path_2) as src2:
        ndvi_1 = src1.read(1).astype(np.float32)
        ndvi_2 = src2.read(1).astype(np.float32)
        
        ndvi_change = ndvi_2 - ndvi_1
        ndvi_change = np.where(~np.isnan(ndvi_1) & ~np.isnan(ndvi_2), ndvi_change, np.nan)
        
        profile = src1.profile
        profile.update(dtype=rasterio.float32, count=1, nodata=np.nan)
        
        with rasterio.open(ndvi_change_path, 'w', **profile) as dst:
            dst.write(ndvi_change, 1)
    
    extent_array = [profile['transform'][2], profile['transform'][2] + profile['width'] * profile['transform'][0], 
                    profile['transform'][5], profile['transform'][5] + profile['height'] * profile['transform'][4]]
    
    plot_ndvi(ndvi_change_path, extent_array, -0.5, 'Spectral', ndvi_change_image)
    plot_ndvi(ndvi_path_1, extent_array, 0, 'YlGn', ndvi_path_1.replace('.tif', '.png'))
    plot_ndvi(ndvi_path_2, extent_array, 0, 'YlGn', ndvi_path_2.replace('.tif', '.png'))
