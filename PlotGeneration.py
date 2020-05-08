import csv
import pandas as pd
import numpy as np
from DataFrame import DataFrame
import plotly


class PlotGeneration:
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
	map_data = pd.read_csv(r"statistics/map_data.csv",
	                       dtype={ fips: str,
	                               state_abbr: str,
	                               state_name: str,
	                               female_incidence: int,
	                               female_mortality: int,
	                               male_incidence: int,
	                               male_mortality: int,
	                               total_incidence: int,
	                               total_mortality: int
	                               })

	@staticmethod
	def calculate_max_value(key):
		max_value = 0
		data_frame = pd.read_csv(r"statistics/map_data.csv",
		                         dtype={ PlotGeneration.fips: str,
		                                 PlotGeneration.state_abbr: str,
		                                 PlotGeneration.female_incidence: str,
		                                 PlotGeneration.female_mortality: str,
		                                 PlotGeneration.male_incidence: str,
		                                 PlotGeneration.male_mortality: str,
		                                 PlotGeneration.total_incidence: str,
		                                 PlotGeneration.total_mortality: str
		                                 })
		for value in data_frame[ key ]:
			if value > max_value:
				max_value = value
		data_frame.close()
		return max_value

	# FemaleMortalityCount and MaleMortalityCount functions will be needed in the DataFrame class
	@staticmethod
	def create_csv():
		# data from https://raw.githubusercontent.com/kjhealy/fips-codes/master/state_fips_master.csv
		data = r"statistics/state_fips_master.csv"
		state_info = pd.read_csv(data, sep=',', header=0, dtype={ 'state_name': str,
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
			filewriter.writerow([ PlotGeneration.fips,
			                      PlotGeneration.state_abbr,
			                      PlotGeneration.state_name,
			                      PlotGeneration.state_population,
			                      PlotGeneration.female_incidence,
			                      PlotGeneration.female_mortality,
			                      PlotGeneration.male_incidence,
			                      PlotGeneration.male_mortality,
			                      PlotGeneration.total_incidence,
			                      PlotGeneration.total_mortality
			                      ])

			# write lines from the state_info github content into the `database` csv file (previous `with open` statement)
			for index in range(len(state_info)):
				row = [ state_info[ 'fips' ][ index ],
				        state_info[ 'state_abbr' ][ index ],
				        state_info[ 'state_name' ][ index ],
				        state_info[ 'state_population' ][ index ],
				        DataFrame.female_incidence[ index ].COUNT,
				        DataFrame.female_mortality[ index ].COUNT,
				        DataFrame.male_incidence[ index ].COUNT,
				        DataFrame.male_mortality[ index ].COUNT,
				        int(DataFrame.female_incidence[ index ].COUNT) + int(DataFrame.male_incidence[ index ].COUNT),
				        int(DataFrame.female_mortality[ index ].COUNT) + int(DataFrame.male_mortality[ index ].COUNT)
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

	@staticmethod
	def generate_choropleth():
		# read data from the map_data CSV file

		#  key       [0]        [1]        [2]
		# {map type: [map_name, bar_title, COLOR_SCALE]}
		map_labels = { 'total_incidence': [ 'Graph 1) Total Incidence Rate', 'Incidence Rate (people)' ],
		               'total_mortality': [ 'Graph 2) Total Mortality Rate', 'Mortality Rate (people)' ],
		               'female_incidence': [ 'Graph 3) Female Incidence Rate', 'Incidence Rate (people)' ],
		               'female_mortality': [ 'Graph 4) Female Mortality Rate', 'Mortality Rat (people)e' ],
		               'male_incidence': [ 'Graph 5) Male Incidence Rate', 'Incidence Rate (people)' ],
		               'male_mortality': [ 'Graph 6) Male Mortality Rate', 'Mortality Rate (people)' ]
		               }

		# generate all map types: total/female/male incidence and mortality
		links = [ ]  # send links to update_html() to update map HTML file location
		for key in map_labels:
			data = dict(type='choropleth',
			            locations=PlotGeneration.map_data[ 'state_abbr' ],
			            locationmode='USA-states',
			            text=PlotGeneration.map_data[ 'state_name' ],
			            zmin=0,
			            zmax=850000,  # 850,000
			            z=PlotGeneration.map_data[ key ],
			            colorscale='agsunset',
			            reversescale=True,
			            colorbar_title=map_labels[ key ][ 1 ])
			layout = dict(title=map_labels[ key ][ 0 ],
			              dragmode=False,
			              geo_scope='usa')

			# save maps
			file_name = r"HTML Files/project_files/%s.html" % key
			choropleth = dict(data=data, layout=layout)

			link = plotly.offline.plot(choropleth,
			                           filename=file_name,
			                           auto_open=False,
			                           show_link=True,
			                           link_text="View on Plotly")
			links.append(link)

		PlotGeneration.update_html(links, "multi")

	"""
	This function will visualize two pie charts. The first will show incidence rate, death rate, and survial rate. Once
	an individual has died from cancer, they are added to the death rate in addition to the incidence rate. This
	may not be correct. In addition, if an individual recovered from cancer, I assume that they are not taken out
	of the incidence rate.

	survival = incidence - death.
	"""

	@staticmethod
	def generate_sankey():
		labels = [ "Total Incidence and Mortality",
		           "Female",
		           "Male",
		           "Incidence",  # Female
		           "Mortality",  # Female
		           "Incidence",  # Male
		           "Mortality" ]  # Male

		colors = [ "#999999",  # Total incidence and mortality
		           "#ff33cc",  # Female
		           "#0066ff",  # Male
		           "#009933",  # Female incidence
		           "#ff0000",  # Female mortality
		           "#009933",  # Male incidence
		           "#ff0000" ]  # Male mortality
		sources = [ 0, 0, 1, 1, 2, 2 ]
		targets = [ 1, 2, 3, 4, 5, 6 ]
		values = PlotGeneration.return_sankey_values()

		data = dict(type='sankey',
		            node=dict(pad=15,
		                      thickness=20,
		                      line=dict(color="black", width=0.5),  # border thickness
		                      label=labels,
		                      color=colors),
		            link=dict(
			            # these are index values from the `label` section under `node`
			            source=sources,
			            target=targets,
			            value=values
		            ))
		layout = dict(title="Mortality and Incidence Visualization")

		file_name = r"HTML Files/project_files/sankey_plot.html"
		sankey = dict(data=data, layout=layout)
		link = [ plotly.offline.plot(sankey,
		                             filename=file_name,
		                             auto_open=False,
		                             show_link=True) ]
		PlotGeneration.update_html(link, "single")

	@staticmethod
	def return_sankey_values():
		female_incidence = np.sum(PlotGeneration.map_data[ 'female_incidence' ])
		female_mortality = np.sum(PlotGeneration.map_data[ 'female_mortality' ])

		male_incidence = np.sum(PlotGeneration.map_data[ 'male_incidence' ])
		male_mortality = np.sum(PlotGeneration.map_data[ 'male_mortality' ])

		total_female = female_incidence + female_mortality
		total_male = male_incidence + male_mortality

		values = [
			total_female,
			total_male,
			female_incidence,
			female_mortality,
			male_incidence,
			male_mortality
		]
		return values

	@staticmethod
	def generate_boxplot():
		data = dict(type='box',
		            boxpoints=[ 1, 2, 3, 4, 5, 6 ])
		layout = dict(title="Mortality and Incidence Visualization")

		boxplot = dict(data=data, layout=layout)
		file_name = r"HTML Files/project_files/boxplot.html"
		link = [ plotly.offline.plot(boxplot,
		                             filename=file_name,
		                             auto_open=False,
		                             show_link=True) ]
		# may need to use plotly.express for this
		PlotGeneration.update_html(link, "single")

	# This function will simply save the HTML file into HTML Files/Project Files
	# number should be "single" or "multi"
	@staticmethod
	def update_html(links: list, number: str):
		# TODO: write each item in links to HTML Files/Project Files so maps are updated if something changes above
		pass
