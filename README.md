## Objective
POI and Analysis
1) Identify commercial centre using Point of Interest (POI) Data in city
2) Create clusters of distinct commercial centre / market
3) Categorise or rank resultant commercial centers by their expected population
4) Visualisation of result
5) Make a Rest API to do any place analysis in flask for better visualisation and interactive dashboard.

**Input** -
1) Data is taken from open street map because -
    - Can use scripts for most of the areas in world
    - Open source Data
    - Crowd source so updated regularly
    - Contains building, land use and street information
2) Input Region -
    - It is defined using Place Name
    Different methods can be defining 
        - Polygon
        - Bounding box
        - circle (point and radius)


**Output** :
1) POI (commercial centres) in ESRI Shapefile Format and geojson format
2) Graphs are made and Final Analysis are saved in CSV for Each Point
3) Rest API in Flask APP
4) buildings.geojson - building of the area
5) network.graphml - Road network of the area
6) commercial poi with cluster class in poi_commercial_clustered_DBSCAN.csv
7) All poi with category in poi_category.csv 
8) commercial poi with population index - more population Index more population
9) poi_data.png for showing all POI
10) street_with_poi.png for showing all POI with street
11) type_of_poi.png to show both commercial and non commercial POI

**Constraints / Notes** ::
1) Assumed population is large where clustering is strong between commercial center
2) Used Spatial Clustering DBSCAN (Density-based spatial clustering)

**Note**: Python code is pep8 compliant

## Tools use 
> Python 3

> Main Libraries Used -
1) osmnx
2) geopandas
3) numpy
4) flask
5) pandas
6) shapely
7) matplotlib
8) scipy
9) scikit-learn

## Installing and Running

> Folders Used -
```sh
$ cd poi_analysis
$ pip install -r requirements.txt
``` 

For Running Flask Application
```sh
$ python webserver.py
```
Use http://0.0.0.0:5000/poiAnalysis/place for web application

For Running model for sample data ('New Delhi')
```sh
$ python model/poi.py
```

## Various Steps in approach are -

1) Data extraction -

    Used Overpass API (http://overpass-api.de/api/interpreter) to get the Data -
    Different type of features and its parameters are extracted depending on open street map
    POI Type used
    - All offices
    - All shops
    - All amenities
    - All leisures
    - All buildings
    - All sports

2) Clustering POI into commercial center/markets by defining tags for each type in separate file.

3) Used Spatial Clustering DBSCAN (Density-based spatial clustering) for clustering POI

4) Used made DBSCAN model to predict commercial center cluster class then rank cluster classes depending on number of commercial center it has and then order all commercial center according to it
Assume  - If commercial center are near to each other or in same spatail cluster we can say population is high. Population Index - more population index more population as compare to other commercial center with low population index

## Future result Can be improve -
1) By using network data for clustering commercial POI by projecting POI on the road and check if accesable.
2) By using building data for tag POI more accurately according to its uses 
2) By using building and its land use data so as to improve clustering to find commercial POI
3) Can use osmnx library to call overpass and handling error when overpass API not respond due to   load using response_json = ox.overpass_request(data={'data':query_str}, timeout=timeout)
4) Better visualisation using flask and leaflet for POI Data
