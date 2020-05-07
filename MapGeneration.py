import csv
import pandas as pd
from DataFrame import DataFrame
import plotly

class MapGeneration:
	# These are the rows found in map_data.csv
	# storing them here makes it easier for both create_csv() and create_map() to access them
	fips = 'fips'
	state_abbr = 'state_abbr'
	state_name = 'state_name'
	female_incidence = 'female_incidence'
	female_mortality = 'female_mortality'
	male_incidence = 'male_incidence'
	male_mortality = 'male_mortality'
	total_incidence = 'total_incidence'
	total_mortality = 'total_mortality'
	state_population = 'state_population'

	@staticmethod
	def calculate_max_value(key):
		max_value = 0
		with open(r"statistics/map_data.csv") as map_data:
			data_frame = pd.read_csv(r"statistics/map_data.csv",
			                         dtype={MapGeneration.fips: str,
			                                MapGeneration.state_abbr: str,
			                                MapGeneration.female_incidence: str,
			                                MapGeneration.female_mortality: str,
			                                MapGeneration.male_incidence: str,
			                                MapGeneration.male_mortality: str,
			                                MapGeneration.total_incidence: str,
			                                MapGeneration.total_mortality: str
			                                })
			for value in data_frame[key]:
				if value > max_value:
					max_value = value
		return max_value


	# FemaleMortalityCount and MaleMortalityCount functions will be needed in the DataFrame class
	@staticmethod
	def create_csv():
		# data from https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_fips_master.csv
		data = r"statistics/state_fips_master.csv"
		state_info = pd.read_csv(data, sep=',', header=0, dtype={'state_name': str,
		                                                         'state_abbr': str,
		                                                         'long_name': str,
		                                                         'fips': str,
		                                                         'sumlev': str,
		                                                         'region': str,
		                                                         'division': str,
		                                                         'state': str,
		                                                         'region_name': str,
		                                                         'division_name': str,
		                                                         'state_population': str
		                                                         })

		# this csv file will act as the database for information on creating the map
		with open(r"statistics/map_data.csv", 'w', newline="") as csvfile:
			filewriter = csv.writer(csvfile, delimiter=',')

			# column headers
			filewriter.writerow([MapGeneration.fips,
			                     MapGeneration.state_abbr,
			                     MapGeneration.state_name,
			                     MapGeneration.state_population,
			                     MapGeneration.female_incidence,
			                     MapGeneration.female_mortality,
			                     MapGeneration.male_incidence,
			                     MapGeneration.male_mortality,
			                     MapGeneration.total_incidence,
			                     MapGeneration.total_mortality
			                     ])

			# write lines from the state_info github content into the `database` csv file (previous `with open` statement)
			for index in range(len(state_info)):
				row = [state_info['fips'][index],
				       state_info['state_abbr'][index],
				       state_info['state_name'][index],
				       state_info['state_population'][index],
				       DataFrame.female_incidence[index].COUNT,
				       DataFrame.female_mortality[index].COUNT,
				       DataFrame.male_incidence[index].COUNT,
				       DataFrame.male_mortality[index].COUNT,
				       int(DataFrame.female_incidence[index].COUNT) + int(DataFrame.male_incidence[index].COUNT),
				       int(DataFrame.female_mortality[index].COUNT) + int(DataFrame.male_mortality[index].COUNT)
				       ]
				filewriter.writerow(row)

	"""
	The following map functions create a map for each of the types of data available, along with each sex (male/female)

	Total incidence map: A choropleth map containing data about the incidences of cancer found within each state
	Total mortality map: A choropleth map containing data about death as a result of cancer found within each state
	Female incidence map: A choropleth map containing data about the incidences of cancer found within each state, for female only
	Female incidence map: A choropleth map containing data about the death as a result of cancer found within each state, for female only
	Male incidence map: A choropleth map containing data about the incidences of cancer found within each state, for male only
	Male incidence map: A choropleth map containing data about the death as a result of cancer found within each state, for male only
	"""
	# TODO: Create a dynamic map to allow the user to select which map they would like to create
	@staticmethod
	def generate_map():
		# read data from the map_data CSV file

		#  key       [0]        [1]        [2]
		# {map type: [map_name, bar_title, COLOR_SCALE]}
		map_labels = {'total_incidence': ['Graph 1) Total Incidence Rate', 'Incidence Rate'],
		              'total_mortality': ['Graph 2) Total Mortality Rate', 'Mortality Rate'],
		              'female_incidence': ['Graph 3) Female Incidence Rate', 'Incidence Rate'],
		              'female_mortality': ['Graph 4) Female Mortality Rate', 'Mortality Rate'],
		              'male_incidence': ['Graph 5) Male Incidence Rate', 'Incidence Rate'],
		              'male_mortality': ['Graph 6) Male Mortality Rate', 'Mortality Rate']
		            }

		map_data = pd.read_csv(r"statistics/map_data.csv",
		                       dtype={MapGeneration.fips: str,
		                              MapGeneration.state_abbr: str,
		                              MapGeneration.state_name: str,
		                              MapGeneration.female_incidence: int,
		                              MapGeneration.female_mortality: int,
		                              MapGeneration.male_incidence: int,
		                              MapGeneration.male_mortality: int,
		                              MapGeneration.total_incidence: int,
		                              MapGeneration.total_mortality: int
		                              })

		# generate all map types: total/female/male incidence and mortality
		links = []  # send links to update_html() to update map HTML file location
		for key in map_labels:
			data = dict(type='choropleth',
			            locations=map_data['state_abbr'],
			            locationmode='USA-states',
			            text=map_data['state_name'],
			            zmin=0,
			            zmax=850000,  # 850,000
			            z=map_data[key],
			            colorscale='agsunset',
			            reversescale=True,
			            colorbar_title=map_labels[key][1])
			layout = dict(title=map_labels[key][0],
			              dragmode=False,
			              geo_scope='usa')

			# save maps
			file_name = r"HTML Files/project_files/%s.html" % key
			choropleth = dict(data=data, layout=layout)

			link = plotly.offline.plot(choropleth,filename=file_name, auto_open=False, show_link=True)
			links.append(link)

		MapGeneration.update_html(links)



	@staticmethod
	def update_html(links):
		write_lines = []
		with open(r"HTML Files\FinalProject.html", 'r') as HTML:
			for line in HTML:
				write_lines.append(line)

		index = 0
		for line in range(len(write_lines)):
			if "frame src" in write_lines[line]:
				new_line = '\t\t\t\t<iframe src="' + links[index][11:] + '" frameborder="5" scrolling="no" width="100%" height="512"> </iframe>\n'
				write_lines[line] = new_line
				index += 1

		with open(r"HTML Files\FinalProject.html", 'w') as HTML:
			for line in write_lines:
				HTML.writelines(line)
