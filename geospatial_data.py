# filename: geospatial_data.py

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import random
from shapely.geometry import Point

def generate_random_points_within_polygon(polygon, num_points):
    points = []
    min_x, min_y, max_x, max_y = polygon.bounds
    
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x), random.uniform(min_y, max_y)])
        if random_point.within(polygon):
            points.append(random_point)
    
    return points

# load world shapefile
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world[world.name != 'Antarctica']
world.crs = 'EPSG:4326'

# generate random points within the world shapefile
num_points = 1000
random_points = generate_random_points_within_polygon(world.unary_union, num_points)

# create a GeoDataFrame with the random points
gdf = gpd.GeoDataFrame(geometry=random_points, crs='EPSG:4326')

# add a 'POPULATION' column with random population values
gdf['POPULATION'] = [random.randint(50000, 500000) for _ in range(len(gdf))]

# filter data
gdf = gdf[gdf['POPULATION'] > 100000]

# reproject to Web Mercator
gdf = gdf.to_crs(epsg=3857)
world = world.to_crs(epsg=3857)

# create a plot
ax = gdf.plot(column='POPULATION', cmap='viridis', legend=True, figsize=(15, 8), markersize=30)

# add a basemap
ctx.add_basemap(ax, zoom=1, source=ctx.providers.Stamen.Terrain)

# set the x and y limits of the plot to match the world shapefile extent
xlim = world.total_bounds[[0, 2]]
ylim = world.total_bounds[[1, 3]]
ax.set_xlim(xlim)
ax.set_ylim(ylim)

# set the aspect of the plot equal to the aspect of the world shapefile in Web Mercator projection
ax.set_aspect('equal')

# set axis labels and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Random Points with Population > 100,000')

# save the plot to the output folder
output_file = 'output/geospatial_plot.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# show the plot
plt.show()
