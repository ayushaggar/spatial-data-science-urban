
# for extracting street network and place boundary
import osmnx as ox
import geopandas as gpd
import time
from shapely.geometry import Point, Polygon
import os
import requests
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import DBSCAN
from scipy.sparse import csr_matrix
import itertools
from scipy import spatial
from model.classification import classification


def call_overpass(data):
    """
    Get Overpass Data

    Parameters
    ----------
    data :
      Overpass Query

    Returns
    Query Data
    """

    # requesting OverPass API
    url = 'http://overpass-api.de/api/interpreter'
    response = requests.post(url, data=data, timeout=180, headers=None)
    response_json = response.json()
    return response_json


def get_buildings(place, polygon):
    """
    Get Buildings Data

    Parameters
    ----------
    place :
      input place
    polygon :
      polygon for Buildings Data

    Returns
    Buildings Data
    """

    max_query_area_size = 3000000000
    maxsize = ''
    timeout = 180

    # requesting polygon geometry and projection
    geometry_proj, crs_proj = ox.project_geometry(polygon)
    # subdividing area if area is big and exceeds max_query_area_size
    geometry_proj_consolidated_subdivided = ox.consolidate_subdivide_geometry(
        geometry_proj, max_query_area_size=max_query_area_size)

    # getting geometry of subpart
    geometry, _ = ox.project_geometry(
        geometry_proj_consolidated_subdivided, crs=crs_proj, to_latlong=True)

    # get polygon coordinates
    polygon_coord_strs = ox.get_polygons_coordinates(geometry)

    print('Requesting building footprint data')
    start_time = time.time()

    # pass each polygon coordinates in the list to Overpass API
    response_jsons = []
    for polygon_coord_str in polygon_coord_strs:
        query_template = ('[out:json][timeout:{timeout}]{maxsize};(way'
                          '(poly:"{polygon}")["building"];(._;>;);relation'
                          '(poly:"{polygon}")["building"];(._;>;););out;')
        query_str = query_template.format(
            polygon=polygon_coord_str,
            timeout=timeout,
            maxsize=maxsize)
        # call overpass API with query
        response_json = call_overpass(data={'data': query_str})
        response_jsons.append(response_json)

    # collectiong Buildings
    vertices = {}
    for response in response_jsons:
        for result in response['elements']:
            if 'type' in result and result['type'] == 'node':
                vertices[result['id']] = {'lat': result['lat'],
                                          'lon': result['lon']}

    buildings = {}
    for response in response_jsons:
        for result in response['elements']:
            if 'type' in result and result['type'] == 'way':
                nodes = result['nodes']
                try:
                    polygon = Polygon(
                        [(vertices[node]['lon'], vertices[node]['lat']) for node in nodes])
                except Exception:
                    print('Polygon has invalid geometry: {}'.format(nodes))
                building = {'nodes': nodes,
                            'geometry': polygon}

                if 'tags' in result:
                    for tag in result['tags']:
                        building[tag] = result['tags'][tag]

                buildings[result['id']] = building

    # converting it into geo pandas
    df_building = gpd.GeoDataFrame(buildings).T
    df_building.crs = {'init': 'epsg:4326'}

    # drop all invalid geometries
    df_building = df_building[df_building['geometry'].is_valid]

    df_building["osm_id"] = df_building.index
    df_building.reset_index(drop=True, inplace=True)
    df_building.gdf_name = str(
        place['state']) + '_buildings' if not place['state'] is None else 'buildings'
    columns_of_interest = [
        "amenity",
        "landuse",
        "leisure",
        "shop",
        "man_made",
        "building",
        "building:use",
        "building:part",
        "osm_id",
        "geometry",
        "height_tags"]

    # drop all unused columns
    df_building.drop([col for col in list(df_building.columns)
                      if col not in columns_of_interest], axis=1, inplace=True)
    return df_building


def get_poi_data(place, polygon):
    """
    Get POI Data

    Parameters
    ----------
    place :
      input place
    polygon :
      polygon for POI Data

    Returns
    POI Data
    """

    max_query_area_size = 3000000000
    maxsize = ''
    timeout = 180

    # requesting polygon geometry and projection
    geometry_proj, crs_proj = ox.project_geometry(polygon)

    # subdividing area if area is big and exceeds max_query_area_size
    geometry_proj_consolidated_subdivided = ox.consolidate_subdivide_geometry(
        geometry_proj, max_query_area_size=max_query_area_size)

    # getting geometry of subpart
    geometry, _ = ox.project_geometry(
        geometry_proj_consolidated_subdivided, crs=crs_proj, to_latlong=True)

    # get polygon coordinates
    polygon_coord_strs = ox.get_polygons_coordinates(geometry)

    print('Requesting POI data')
    start_time = time.time()

    # pass each polygon coordinates in the list to Overpass API
    response_jsons = []
    for polygon_coord_str in polygon_coord_strs:
        query_template = ('[out:json][timeout:{timeout}]{maxsize};('
                          '(node["office"](poly:"{polygon}"););'
                          '(node["shop"](poly:"{polygon}"););'
                          '(node["amenity"](poly:"{polygon}"););'
                          '(node["leisure"](poly:"{polygon}"););'
                          '(node["building"](poly:"{polygon}"););'
                          '(node["sport"](poly:"{polygon}");););out;')
        query_str = query_template.format(
            polygon=polygon_coord_str,
            timeout=timeout,
            maxsize=maxsize)
        # call overpass API with query
        response_json = call_overpass(data={'data': query_str})
        response_jsons.append(response_json)

    # collectiong POI
    vertices = {}
    for response in response_jsons:
        for result in response['elements']:
            if 'type' in result and result['type'] == 'node':

                point = Point(result['lon'], result['lat'])

                POI = {'geometry': point}

                if 'tags' in result:
                    for tag in result['tags']:
                        POI[tag] = result['tags'][tag]

                vertices[result['id']] = POI

    # converting it into geo pandas
    df_poi = gpd.GeoDataFrame(vertices).T
    df_poi.crs = {'init': 'epsg:4326'}

    try:
        # drop all invalid geometries
        df_poi = df_poi[df_poi['geometry'].is_valid]
    except BaseException:
        # Empty data frame
        # Create one-row data frame with null information
        point = polygon.centroid
        data = {"geometry": [point], "osm_id": [0]}
        df_poi = gpd.GeoDataFrame(data, crs={'init': 'epsg:4326'})

    df_poi["osm_id"] = df_poi.index
    df_poi.reset_index(drop=True, inplace=True)
    df_poi.gdf_name = str(
        place['state']) + '_points' if not place['state'] is None else 'points'
    columns_of_interest = [
        "amenity",
        "landuse",
        "leisure",
        "shop",
        "man_made",
        "building",
        "building:use",
        "building:part",
        "osm_id",
        "geometry"]

    # drop all unused columns
    df_poi.drop([col for col in list(df_poi.columns)
                 if col not in columns_of_interest], axis=1, inplace=True)
    return df_poi


def get_polygon(place):
    """
    Get Polygon

    Parameters
    ----------
    df_osm_data : geopandas.GeoDataFrame
      input OSM data frame
    geo_filename : string
      filename for GeoDataFrame storage

    Returns
    Polygon
    """

    # Get polygon
    poly_gdf = ox.gdf_from_place(place, which_result=1)
    polygon = poly_gdf.geometry[0]
    return polygon


def store_geodataframe(df_osm_data, geo_filename):
    """
    Store input GeoDataFrame

    Parameters
    ----------
    df_osm_data : geopandas.GeoDataFrame
      input OSM data frame
    geo_filename : string
      filename for GeoDataFrame storage

    Returns
    ------

    """
    # To EPSG 4326 - Project GeoDataFrame to the UTM zone
    df_osm_data = ox.project_gdf(df_osm_data, to_latlong=True)
    # Save to file
    df_osm_data.to_file(geo_filename, driver='GeoJSON')


def load_geodataframe(geo_filename):
    """
    Load input GeoDataFrame

    Parameters
    ----------
    geo_filename : string
      filename for GeoDataFrame storage

    Returns
    df_osm_data : geopandas.GeoDataFrame
      output OSM data frame
    """

    # Load using geopandas
    df_osm_data = gpd.read_file(geo_filename)

    # Replace None as NaN
    df_osm_data.fillna(value=np.nan, inplace=True)

    # Replace empty string for NaN
    df_osm_data.replace('', np.nan, inplace=True)

    # To UTM coordinates
    return df_osm_data


def poi_cluster(df_poi, path_to_output):
    poi_data = pd.DataFrame(
        {'x': df_poi.geometry.x, 'y': df_poi.geometry.y, 'amenity': df_poi.amenity})
    file_input_path = path_to_output + '/poi_category.csv'

    file_path = path_to_output + '/poi_commercial_clustered_DBSCAN.csv'
    file_path_2 = path_to_output + '/poi_commercial_population_index.csv'

    poi_data = pd.read_csv(file_input_path, encoding='utf-8')

    # parameterize DBSCAN
    eps = 300  # meters
    minpts = 5  # smallest cluster size allowed
    eps_rad = eps / 3671000.  # meters to radians
    db = DBSCAN(
        eps=eps_rad,
        min_samples=minpts,
        metric='haversine',
        algorithm='ball_tree')

    # predicting and assigning each cmmercial point to cluster
    poi_data = poi_data[poi_data.category == 'commercial']
    poi_data['spatial_cluster'] = db.fit_predict(
        np.deg2rad(poi_data[['y', 'x']]))

    # save clustered POI data set
    poi_data.to_csv(file_path, encoding='utf-8', index=False)

    # Calculating Population Index
    # more population index more population as compare to other commercial
    # center with low population index
    poi_data['count'] = 1
    cluster_count = poi_data.groupby(
        ['spatial_cluster'])['count'].sum().reset_index().sort_values(
        by=['count'], ascending=False)
    poi_data = poi_data.drop(['count'], 1)
    commercial_cluster_population_index = pd.merge(
        poi_data,
        cluster_count,
        on='spatial_cluster',
        how='inner').sort_values(
        by=['count'],
        ascending=False)
    commercial_cluster_population_index = commercial_cluster_population_index.drop([
                                                                                   'spatial_cluster'], 1)
    commercial_cluster_population_index.rename(
        columns={
            'count': 'population_index'},
        inplace=True)
    commercial_cluster_population_index.to_csv(
        file_path_2, encoding='utf-8', index=False)


def poi_street(df_poi, path_to_output):
    street_file = path_to_output + '/network.graphml'
    image_path = path_to_output + '/street_with_poi.png'

    street_data = ox.load_graphml(street_file)
    poi_data = pd.DataFrame(
        {'x': df_poi.geometry.x, 'y': df_poi.geometry.y, 'amenity': df_poi.amenity})

    # plot the poi data and street
    fig, ax = ox.plot_graph(street_data, node_color='#ff3300',
                            edge_color='#aaaaaa', node_size=0, show=False, close=True, dpi=600)
    ax.scatter(
        x=poi_data['x'],
        y=poi_data['y'],
        c='blue',
        marker='.',
        s=40,
        zorder=3,
        label='POI')
    ax.legend(title="LEGEND")
    ax.set(title='POI with Street')
    ax.set(xlabel='Longitude')
    ax.set(ylabel='Latitude')
    ax.grid(True)
    fig.savefig(image_path, dpi=600)


def poi_image(df_poi, path_to_output):
    image_path = path_to_output + '/poi_data.png'
    fig, ax = plt.subplots(figsize=(10, 10))
    df_poi.plot(ax=ax, label='POI', color="blue")
    ax.legend(title="LEGEND")
    ax.set(title='POI Data')
    ax.set(xlabel='Longitude')
    ax.set(ylabel='Latitude')
    # ax.set_axis_off()
    fig.savefig(image_path, dpi=600)


def poi_classification(df_poi, path_to_output):
    image_path = path_to_output + '/type_of_poi.png'
    file_path = path_to_output + '/poi_category.csv'

    df_poi['classification'], df_poi['key_value'] = list(
        zip(*df_poi.apply(classification.classify_tag, axis=1)))
    # Remove unnecessary POIs
    df_poi.drop(df_poi[df_poi.classification.isin(
        ["infer", "other"]) | df_poi.classification.isnull()].index, inplace=True)
    df_poi.reset_index(inplace=True, drop=True)

    # Assigning commercial or non commercial tag depending on POIs
    df_poi['category'] = df_poi.apply(
        lambda x: classification.classify_activity_category(
            x.key_value), axis=1)
    poi_data = pd.DataFrame({'x': df_poi.geometry.x,
                             'y': df_poi.geometry.y,
                             'amenity': df_poi.amenity,
                             'classification': df_poi.classification,
                             'key_value': df_poi.key_value,
                             'category': df_poi.category.str[0]})
    poi_data.to_csv(file_path, encoding='utf-8', index=False)

    # for visualisation of categories
    df_pois_commercial = df_poi[df_poi.category.str[0].isin(["commercial"])]
    df_pois_non_commercial = df_poi[df_poi.category.str[0].isin(
        ["non_commercial"])]
    fig, ax = plt.subplots(figsize=(10, 10))
    df_pois_commercial.plot(ax=ax, label='commercial', color="blue")
    df_pois_non_commercial.plot(ax=ax, label='non_commercial', color="red")
    ax.legend(title="LEGEND")
    ax.set(title='POI Classification')
    ax.set(xlabel='Longitude')
    ax.set(ylabel='Latitude')
    fig.savefig(image_path, dpi=600)


def analyse_data(place, path_to_output):
    place_ref = str(place['state'])
    path_to_output = data_path
    poi_file = path_to_output + '/poi.geojson'

    df_poi = load_geodataframe(poi_file)

    # saving POI as image
    poi_image(df_poi, path_to_output)

    # Classification of POI and saving as image
    poi_classification(df_poi, path_to_output)

    # POI analyse using street of city
    poi_street(df_poi, path_to_output)

    # POI spatial clustering
    poi_cluster(df_poi, path_to_output)


def download_data(place, data_path):

    place_ref = str(place['state'])
    print('OSM data requested for city: ' + str(place_ref))
    path_to_output = data_path

    # if folder not exist create folder with place name
    if not(os.path.isdir(path_to_output)):
        os.makedirs(path_to_output)

    poi_file = path_to_output + '/poi.geojson'
    building_file = path_to_output + '/buildings.geojson'
    street_file = path_to_output + '/network.graphml'

    # Requesting polygon of place
    polygon = get_polygon(place)

    # Requesting POI data within polygon
    poi_data = get_poi_data(place, polygon)
    # saving POI data as geojson
    store_geodataframe(poi_data, poi_file)

    # Requesting building data of city using polygon
    buildings_data = get_buildings(place, polygon)
    # saving building data as geojson
    store_geodataframe(buildings_data, building_file)

    # Requesting street network using polygon
    street_data = ox.graph_from_polygon(polygon, network_type='drive')
    # Save street network as GraphML file
    ox.save_graphml(street_data, filename=street_file)

    print('Stored OSM data files for city: ' + place_ref)


def main(input_place, data_path):
    place = {'state': input_place,
             'country': 'India'}
    download_data(place, data_path)
    analyse_data(place, data_path)

    return 'Done'


if __name__ == "__main__":
    print ('direct executed')
    input_place = 'New Delhi'
    data_path = os.path.join(os.getcwd(), 'result_data')
    main(input_place, data_path)
else:
    print ('imported')
