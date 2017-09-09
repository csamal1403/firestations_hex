import json
import csv
import numpy as np 
from scipy.spatial import cKDTree

def getHexCellOfIncident(list_of_latitudes, list_of_longitudes, polygons):
	hexCells = []
	verts = []
	centroids = []

	for hexagon in polygons['features']:
		xy = np.array(hexagon['geometry']['coordinates'][0][:6])
		verts.append(xy)

		centroids.append(xy.mean(0))

	verts = np.array(verts)
	centroids = np.array(centroids)

	tree = cKDTree(centroids)

	index = 0

	xy = np.zeros((len(list_of_latitudes), 2))
	for i in range(len(list_of_latitudes)):
		xy[index][0] = list_of_longitudes[i]
		xy[index][1] = list_of_latitudes[i]
		index = index + 1

	distance, idx = tree.query(xy, 1)
	hexCells = idx.tolist()
	return hexCells



def process_csv(csv_file):

	nyc_lats = []
	nyc_lngs = []
	nj_lats = []
	nj_lngs = []
	nyc_rows = []
	nj_rows = []

	# Do the reading
	file1 = open(csv_file, 'rb')
	reader = csv.reader(file1)
	for row in reader:
		lng = row[2]
		lat = row[3]
		if row[1] == 'NY':
			nyc_lats.append(lat)
			nyc_lngs.append(lng)
			nyc_rows.append(row)

		elif row[1] == 'NJ':
			nj_lats.append(lat)
			nj_lngs.append(lng)
			nj_rows.append(row)

	file1.close()

	nyc_polygons = readGeoJSON('nyc_hex.geojson')
	nj_polygons = readGeoJSON('nj_hex.geojson')

	nyc_hex_cells = getHexCellOfIncident(nyc_lats, nyc_lngs, nyc_polygons)
	nj_hex_cells = getHexCellOfIncident(nj_lats, nj_lngs, nj_polygons)

	new_nyc_rows_list = []
	new_nj_rows_list = []

	for nyc_row_index in range(len(nyc_rows)):
		nyc_row = nyc_rows[nyc_row_index]
		new_nyc_row = [nyc_row[0], nyc_row[1], nyc_row[2], nyc_row[3], nyc_hex_cells[nyc_row_index]]
		new_nyc_rows_list.append(new_nyc_row)

	for nj_row_index in range(len(nj_rows)):
		nj_row = nj_rows[nj_row_index]
		new_nj_row = [nj_row[0], nj_row[1], nj_row[2], nj_row[3], nj_hex_cells[nj_row_index]]
		new_nj_rows_list.append(new_nj_row)


	# # Do the writing
	nyc_file = open('nyc_fire_stations_with_hex.csv', 'wb')
	nyc_writer = csv.writer(nyc_file)
	nyc_writer.writerows(new_nyc_rows_list)
	nyc_file.close()

	nj_file = open('nj_fire_stations_with_hex.csv', 'wb')
	nj_writer = csv.writer(nj_file)
	nj_writer.writerows(new_nj_rows_list)
	nj_file.close()



def readGeoJSON(filename):
	with open(filename) as f:
		data = json.load(f)
	return data 


def main():
	process_csv('fire_stations_nyc_nj.csv')


if __name__ == '__main__':
	main()