#!/usr/bin/env python3

# Simon's Travel Tracker
# Testing out Folium for Geovisualization

import sys
import os
import glob

import folium
from geopy.geocoders import Nominatim

sys.path.insert(0, './external_plugins')
import Externals

import pandas

import branca.colormap as cm

def main():
	locations_dir = './locations/'
	visited_cities_list = 'visited-cities.csv'
	nvisited_cities_list = 'want-to-visit.csv'
	visited_geos_dir = '{}{}'.format(locations_dir, 'visited/')
	nvisited_geos_dir = '{}{}'.format(locations_dir, 'want-to-visit/')

	# Get Lat and Long of cities
	geolocator = Nominatim(timeout=1000000)

	# For cities that I have vistied
	visited_lats_longs = []
	visited_cities = []

	# For cities I want to visit
	nvisited_lats_longs = []
	nvisited_cities = []

	visited_df = pandas.read_csv(
		'{}{}'.format(
			locations_dir,
			visited_cities_list),
		sep=',')
	visited_rows = visited_df.shape[0]

	nvisited_df = pandas.read_csv(
		'{}{}'.format(
			locations_dir,
			nvisited_cities_list),
		sep=',')
	nvisited_rows = nvisited_df.shape[0]

	# Add the cities I've visited to a list
	print("Visited Cities:")
	for x in range(visited_rows):
		d = visited_df.iloc[x]['Visited Cities']
		print(d)
		visited_cities.append(d)

	# Add the cities that I want to visit to a list
	print("\nCities I Want to Visit")
	for x in range(nvisited_rows):
		d = nvisited_df.iloc[x]['Want to Visit']
		print(d)
		nvisited_cities.append(d)

	# Get the latitude and logitude of cities I have visited
	print("\nCoordinates of cities I have visited")
	for city in visited_cities:
		location = geolocator.geocode(city)
		print(location)
		visited_lats_longs.append([location.latitude, location.longitude])

	# Get the latitude and logitudes of cities that I want to visit
	print("\nCoordinates of cities I want to visit")
	for city in nvisited_cities:
		location = geolocator.geocode(city)
		print(location)
		nvisited_lats_longs.append([location.latitude, location.longitude])


	# Sanity check
	for result in visited_lats_longs:
		print(result[0], result[1])

	for result in nvisited_lats_longs:
		print(result[0], result[1])

	# Note: Need to confirm differente between add_child and add_to

	f = folium.Figure(width=1000, height=500)  # Instantiate a figure
	travel_map = folium.Map(location=[0, 0], zoom_start=2, min_zoom=2).add_to(
		f)  # Instantiate a world map and add it to the figure
	# Add Latitude Longitude Popup to the map
	travel_map.add_child(folium.features.LatLngPopup())
	fs = Externals.Fullscreen()
	szt = Externals.ScrollZoomToggler()

	fs.add_to(travel_map)  # Add a Fullscreen button to the map (plugin)
	# Add the scroll zoom toggler button to the map (plugin)
	szt.add_to(travel_map)

	# Colorscale: Steps of 10 between 0 and 200
	colorscale = cm.linear.PuRd.scale(0, 200)
	colorscale.caption = 'Total number of days spent in each location (Coming Soon)'
	travel_map.add_child(colorscale)

	"""
	Add the .geo.json data for countries to the map first
	"""
	# Get *.geo.json for visited countries
	for root, dirs, files in os.walk(visited_geos_dir):
		visited_jsons = files
		print(visited_jsons)

	# Get *.geo.json for countries not visited
	for root, dirs, files in os.walk(nvisited_geos_dir):
		nvisited_jsons = files
		print(nvisited_jsons)

	# Create feature groups for the countries
	visited_map_countries = folium.FeatureGroup(name='Countries I\'ve Visited')
	nvisited_map_countries = folium.FeatureGroup(name='Countries I want to visit')

	y = 0  # Indexing for countries that I haven't visited
	for x in range(0, len(visited_jsons) + len(nvisited_jsons)):
		if x < len(visited_jsons):  # For visited countries
			map_loc = folium.GeoJson(
				open(
					'{}{}'.format(
						visited_geos_dir,
						visited_jsons[x]),
					encoding="utf-8-sig").read(),
				style_function=lambda x: {
					'fillColor': 'green',
					'dashArray': '5, 5'},
				highlight_function=lambda x: {
					'weight': 2,
					'fillColor': 'blue'})  # Load the .geo.json data and customize
			# Add the GeoJSON to the map_countries feature group
			visited_map_countries.add_child(map_loc)

		else:  # For countries not yet visited
			map_loc = folium.GeoJson(
				open(
					'{}{}'.format(
						nvisited_geos_dir,
						nvisited_jsons[y]),
					encoding="utf-8-sig").read(),
				style_function=lambda x: {
					'fillColor': 'red',
					'dashArray': '5, 5'},
				highlight_function=lambda x: {
					'weight': 2,
					'fillColor': 'blue'})  # Load the .geo.json data and customize
			# Add the GeoJSON to the map_countries feature group
			nvisited_map_countries.add_child(map_loc)
			y += 1

	visited_map_countries.add_to(travel_map)  # Add the feature group to the map
	nvisited_map_countries.add_to(travel_map)  # Add the feature group to the map

	"""
	Next, add the processed geopy data for cities
	"""
	visited_map_cities = folium.FeatureGroup(name='Cities I\'ve Visited')
	nvisited_map_cities = folium.FeatureGroup(name='Cities I want to visit')

	y = 0  # Indexing for cities that I haven't visited
	for x in range(0, len(visited_lats_longs) + len(nvisited_lats_longs)):
		if x < len(visited_lats_longs):  # For visited cities
			mkr = folium.Marker(
				[
					visited_lats_longs[x][0],
					visited_lats_longs[x][1]],
				popup=visited_df.iloc[x]['Visited Cities'],
				icon=folium.Icon(
					color='green',
					prefix='fa',
					icon='plane'))  # Add a marker to show the name of the city located at the marker on click
			# Add the marker to the feature group
			visited_map_cities.add_child(mkr)
		else:  # For cities not yet visited
			mkr = folium.Marker(
				[
					nvisited_lats_longs[y][0],
					nvisited_lats_longs[y][1]],
				popup=nvisited_df.iloc[y]['Want to Visit'],
				icon=folium.Icon(
					color='red',
					prefix='fa',
					icon='plane'))  # Add a marker to show the name of the city located at the marker on click
			# Add the marker to the feature group
			nvisited_map_cities.add_child(mkr)
			y += 1

	visited_map_cities.add_to(travel_map)  # Add the feature group to the map
	nvisited_map_cities.add_to(travel_map)  # Add the feature group to the map

	folium.LayerControl().add_to(travel_map)  # Add Layer Controller to the map

	# Add a legend
	legend_html = '''
		<div style="position: fixed;
			bottom: 50px; left: 50px; width: 100px; height: 90px;
			border:2px solid grey; z-index:9999; font-size:14px;
			">&nbsp; Legend <br>
			  &nbsp; Visited &nbsp; <i class="fa fa-map-marker fa-2x" style="color:green"></i><br>
			  &nbsp; Will Visit &nbsp; <i class="fa fa-map-marker fa-2x" style="color:red"></i>
		</div>
	'''
	travel_map.get_root().html.add_child(folium.Element(legend_html))

	travel_map.save('index.html')

if __name__ == '__main__':
	main()
