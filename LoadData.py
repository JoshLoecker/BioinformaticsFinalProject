from DataFrame import DataFrame
import pandas as pd
def load_data():

	with open(r"statistics/state_fips_master.csv") as states:
		state_list = pd.read_csv(states, sep=',', header=0, dtype={'state_name': str,
		                                                           'state_abbr': str,
		                                                           'long_name': str,
		                                                           'fips': str,
		                                                           'sumlev': str,
		                                                           'region': str,
		                                                           'division': str,
		                                                           'state': str,
		                                                           'region_name': str,
		                                                           'division_name': str
		                                                           })
		for line in state_list['state_name']:
			DataFrame.state_list.append(line)

	# open the data file BYAREA.txt in read mode
	with open(DataFrame.data_file, mode='r') as readcsv:
		index = 0

		# for each line in the file
		for line in readcsv:

			# skip the first line (contains headers)
			if index == 0:
				index = index + 1
			else:
				# split the line by pipe `|` symbol into list
				class_instance = line.rstrip("\n").split("|")

				# take each index in list and load it into a DataFrame
				# append this DataFrame into class_array
				DataFrame.class_instances.append(DataFrame(class_instance[0],  # AREA
				                                           class_instance[1],  # AGE_ADJUSTED_CI_LOWER
				                                           class_instance[2],  # AGE_ADJUSTED_CI_UPPER
				                                           class_instance[3],  # AGE_ADJUSTED_RATE
				                                           class_instance[4],  # COUNT
				                                           class_instance[5],  # EVENT_TYPE
				                                           class_instance[6],  # POPULATION
				                                           class_instance[7],  # RACE
				                                           class_instance[8],  # SEX
				                                           class_instance[9],  # SITE
				                                           class_instance[10],  # YEAR
				                                           class_instance[11],  # CRUDE_CI_LOWER
				                                           class_instance[12],  # CRUDE_CI_UPPER
				                                           class_instance[13]))  # CRUDE_RATE
