"""Functions for creating interactive maps of hydro-topological features."""

import os
import logging
from pathlib import Path
from io import BytesIO
import base64
from typing import Dict, List, Optional, Union, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import rasterio
import geopandas as gpd
import folium
from folium import plugins
from folium.raster_layers import ImageOverlay
from matplotlib import cm
from .. import config

logger = logging.getLogger(__name__)

def plot_interactive_map(
    site_id: str,
    raster_paths: list,
    aoi_path: str = None,
    Name: list = None,
    Unit: list = None,
    vmin: list = None,
    vmax: list = None,
    cmap: list = None,
    cbar_titles: list = None,
    opacity: float = None,
    zoom_start: int = None,
    output_dirs: Optional[Dict[str, Path]] = None
) -> str:
    """
    Create an interactive map with multiple raster layers.
    
    Args:
        site_id: Unique identifier for the site
        raster_paths: List of paths to raster files
        aoi_path: Path to AOI shapefile/geopackage
        Name: List of names for each raster layer
        Unit: List of units for each raster layer
        vmin: List of minimum values for each raster
        vmax: List of maximum values for each raster
        cmap: List of colormaps for each raster
        cbar_titles: List of colorbar titles (overrides automatic construction)
        opacity: Opacity for raster layers
        zoom_start: Initial zoom level
        output_dirs: Dictionary of output directories
        
    Returns:
        Path to the output interactive map
    """
    logger.info(f"Creating interactive map for site: {site_id}")
    
    # Default values if None
    if Name is None:
        Name = [f"Layer {i+1}" for i in range(len(raster_paths))]
    if Unit is None:
        Unit = [""] * len(raster_paths)
    if vmin is None:
        vmin = [None] * len(raster_paths)
    if vmax is None:
        vmax = [None] * len(raster_paths)
    if cmap is None:
        cmap = ["terrain"] * len(raster_paths)
    if cbar_titles is None:
        cbar_titles = [""] * len(raster_paths)
    
    # Set defaults from config
    vis_config = config.INTERACTIVE_VIS
    opacity = opacity if opacity is not None else vis_config['opacity']
    zoom_start = zoom_start if zoom_start is not None else vis_config['zoom_start']
    
    # Get center coordinates from first raster
    with rasterio.open(raster_paths[0]) as src:
        bounds = rasterio.transform.array_bounds(src.height, src.width, src.transform)
        miny, minx, maxy, maxx = bounds[1], bounds[0], bounds[3], bounds[2]
        center_lat = (miny + maxy) / 2
        center_lon = (minx + maxx) / 2
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        control_scale=True
    )
    
    # Add each raster layer
    for i, raster_path in enumerate(raster_paths):
        with rasterio.open(raster_path) as src:
            data = src.read(1)
            bounds = rasterio.transform.array_bounds(src.height, src.width, src.transform)
            miny, minx, maxy, maxx = bounds[1], bounds[0], bounds[3], bounds[2]
            
            # Handle nodata values
            nodata = src.nodata if src.nodata is not None else config.DEM_PROCESSING["NODATA_VALUE"]
            data = np.ma.masked_where(data == nodata, data)
            
            # Get value range
            v_min = vmin[i] if i < len(vmin) and vmin[i] is not None else float(np.nanmin(data))
            v_max = vmax[i] if i < len(vmax) and vmax[i] is not None else float(np.nanmax(data))
            
            # Clip values to range
            clipped_data = np.clip(data, v_min, v_max)
            
            # Normalize data
            normed_data = (clipped_data - v_min) / (v_max - v_min) if v_max > v_min else np.zeros_like(clipped_data)
            
            # Apply colormap
            cmap_name = cmap[i] if i < len(cmap) else 'terrain'
            colormap = getattr(cm, cmap_name)
            colored_data = colormap(normed_data)[:, :, :3]
            colored_data = (colored_data * 255).astype(np.uint8)
            
            # Add layer to map
            layer_name = Name[i] if i < len(Name) else f"Layer {i+1}"
            img = ImageOverlay(
                image=colored_data,
                bounds=[[miny, minx], [maxy, maxx]],
                opacity=opacity,
                name=layer_name
            )
            img.add_to(m)
            
            # Create colorbar
            fig, ax = plt.subplots(figsize=(1.5, 4))
            norm = plt.Normalize(vmin=v_min, vmax=v_max)
            cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap_name), cax=ax)
            
            # Add label to colorbar
            unit_str = Unit[i] if i < len(Unit) else ""
            cbar_title_str = cbar_titles[i] if i < len(cbar_titles) and cbar_titles[i] else ""
            
            if cbar_title_str:
                cbar.set_label(cbar_title_str)
            elif unit_str:
                cbar.set_label(f"{unit_str}")
            
            plt.tight_layout()
            
            # Save colorbar to BytesIO
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            
            # Add colorbar to map
            colorbar_html = f'''
                <div style="
                    position: fixed; 
                    bottom: 50px; 
                    right: {50 + i*100}px; 
                    z-index: 9999; 
                    background-color: white;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.5);">
                    <p style="text-align:center; margin:0; font-weight:bold;">{layer_name}</p>
                    <img src="data:image/png;base64,{img_str}" style="height:200px;">
                </div>
            '''
            m.get_root().html.add_child(folium.Element(colorbar_html))
    
    # Add AOI if provided
    if aoi_path:
        aoi = gpd.read_file(aoi_path)
        if aoi.crs != 'EPSG:4326':
            aoi = aoi.to_crs('EPSG:4326')
        
        folium.GeoJson(
            aoi,
            name='Area of Interest',
            style_function=lambda x: {
                'color': vis_config['aoi_color'],
                'weight': vis_config['aoi_weight'],
                'dashArray': vis_config['aoi_dash_array'],
                'fillOpacity': vis_config['aoi_fill_opacity']
            }
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Set output path
    if output_dirs is None:
        output_path = f"{site_id}_interactive_map.html"
    else:
        output_path = output_dirs["interactive_figures"] / f"{site_id}_interactive_map.html"
    
    # Save map
    os.makedirs(os.path.dirname(str(output_path)), exist_ok=True)
    m.save(str(output_path))
    logger.info(f"Interactive map saved to: {output_path}")
    return str(output_path)

def create_interactive_map(
    site_id: str,
    layers: List[str],
    layer_paths: List[str],
    layer_names: List[str],
    cmaps: List[str],
    vmins: List[float],
    vmaxs: List[float],
    Unit: List[str],
    cbar_titles: List[str] = None,
    aoi_path: str = None,
    world_topo: bool = True,
    map_center: Tuple[float, float] = None,
    zoom_start: int = 10,
    output_path: Optional[str] = None
) -> str:
    """
    Create an interactive map with multiple layers.
    
    Args:
        site_id: Site identifier
        layers: List of layer identifiers
        layer_paths: List of paths to raster layers
        layer_names: List of layer names for display
        cmaps: List of colormaps for each layer
        vmins: List of minimum values for color scaling
        vmaxs: List of maximum values for color scaling
        Unit: List of units for each layer
        cbar_titles: List of colorbar titles (overrides automatic construction)
        aoi_path: Path to the AOI shapefile (optional)
        world_topo: Whether to include a world topo layer
        map_center: Center coordinates for the map (lat, lon)
        zoom_start: Initial zoom level
        output_path: Path to save the interactive map
        
    Returns:
        Path to the saved interactive map
    """
    # Use empty list if cbar_titles is None
    if cbar_titles is None:
        cbar_titles = [""] * len(layers)

    # Use default map center if not provided
    if map_center is None:
        map_center = (0, 0)

    # Use default zoom start if not provided
    if zoom_start is None:
        zoom_start = 10

    # Use default output path if not provided
    if output_path is None:
        output_path = f"{site_id}_interactive_map.html"

    logger.info(f"Creating interactive map for site: {site_id}")
    
    # Set defaults from config
    vis_config = config.INTERACTIVE_VIS
    opacity = vis_config['opacity']
    zoom_start = zoom_start
    
    # Get center coordinates from first raster
    with rasterio.open(layer_paths[0]) as src:
        bounds = rasterio.transform.array_bounds(src.height, src.width, src.transform)
        miny, minx, maxy, maxx = bounds[1], bounds[0], bounds[3], bounds[2]
        center_lat = (miny + maxy) / 2
        center_lon = (minx + maxx) / 2
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        control_scale=True
    )
    
    # Add each raster layer
    for i, layer_path in enumerate(layer_paths):
        with rasterio.open(layer_path) as src:
            data = src.read(1)
            bounds = rasterio.transform.array_bounds(src.height, src.width, src.transform)
            miny, minx, maxy, maxx = bounds[1], bounds[0], bounds[3], bounds[2]
            
            # Handle nodata values
            nodata = src.nodata if src.nodata is not None else config.DEM_PROCESSING["NODATA_VALUE"]
            data = np.ma.masked_where(data == nodata, data)
            
            # Get value range
            v_min = vmins[i] if i < len(vmins) and vmins[i] is not None else float(np.nanmin(data))
            v_max = vmaxs[i] if i < len(vmaxs) and vmaxs[i] is not None else float(np.nanmax(data))
            
            # Clip values to range
            clipped_data = np.clip(data, v_min, v_max)
            
            # Normalize data
            normed_data = (clipped_data - v_min) / (v_max - v_min) if v_max > v_min else np.zeros_like(clipped_data)
            
            # Apply colormap
            cmap_name = cmaps[i] if i < len(cmaps) else 'terrain'
            colormap = getattr(cm, cmap_name)
            colored_data = colormap(normed_data)[:, :, :3]
            colored_data = (colored_data * 255).astype(np.uint8)
            
            # Add layer to map
            layer_name = layer_names[i] if i < len(layer_names) else f"Layer {i+1}"
            img = ImageOverlay(
                image=colored_data,
                bounds=[[miny, minx], [maxy, maxx]],
                opacity=opacity,
                name=layer_name
            )
            img.add_to(m)
            
            # Create colorbar
            fig, ax = plt.subplots(figsize=(1.5, 4))
            norm = plt.Normalize(vmin=v_min, vmax=v_max)
            cbar = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap_name), cax=ax)
            
            # Add label to colorbar
            unit_str = Unit[i] if i < len(Unit) else ""
            cbar_title = cbar_titles[i] if i < len(cbar_titles) and cbar_titles[i] else ""
            
            if cbar_title:
                cbar.set_label(cbar_title)
            elif unit_str:
                cbar.set_label(f"{unit_str}")
            
            plt.tight_layout()
            
            # Save colorbar to BytesIO
            buf = BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight', dpi=100)
            plt.close()
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            
            # Add colorbar to map
            colorbar_html = f'''
                <div style="
                    position: fixed; 
                    bottom: 50px; 
                    right: {50 + i*100}px; 
                    z-index: 9999; 
                    background-color: white;
                    padding: 10px;
                    border-radius: 5px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.5);">
                    <p style="text-align:center; margin:0; font-weight:bold;">{layer_name}</p>
                    <img src="data:image/png;base64,{img_str}" style="height:200px;">
                </div>
            '''
            m.get_root().html.add_child(folium.Element(colorbar_html))
    
    # Add AOI if provided
    if aoi_path:
        aoi = gpd.read_file(aoi_path)
        if aoi.crs != 'EPSG:4326':
            aoi = aoi.to_crs('EPSG:4326')
        
        folium.GeoJson(
            aoi,
            name='Area of Interest',
            style_function=lambda x: {
                'color': vis_config['aoi_color'],
                'weight': vis_config['aoi_weight'],
                'dashArray': vis_config['aoi_dash_array'],
                'fillOpacity': vis_config['aoi_fill_opacity']
            }
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Save map
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    m.save(output_path)
    logger.info(f"Interactive map saved to: {output_path}")
    return str(output_path) 