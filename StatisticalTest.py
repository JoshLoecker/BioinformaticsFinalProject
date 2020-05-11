import numpy as np
import pandas as pd
import scipy.stats as stats


class StatisticalTest:
	fips = 'fips'
	state_abbr = 'state_abbr'
	state_name = 'state_name'
	female_incidence = 'female_incidence'
	female_mortality = 'female_mortality'
	male_incidence = 'male_incidence'
	male_mortality = 'male_mortality'
	total_incidence = 'total_incidence'
	total_mortality = 'total_mortality'
	data_frame = pd.read_csv(r'statistics/map_data.csv',
	                         sep=',',
	                         header=0,
	                         dtype={fips: str,
	                                state_abbr: str,
	                                female_incidence: int,
	                                female_mortality: int,
	                                male_incidence: int,
	                                male_mortality: int,
	                                total_incidence: int,
	                                total_mortality: int
	                                })

	def __init__(self):
		"""
		This will simply collect values needed for later tests.
		"""
		values = self.return_values()
		self.calculate_ANOVA_test(values)

	@staticmethod
	def return_values():
		"""
		This function will collect the female and male mortality and incidence rates from the map_data.csv file
		:return: female_incidence: list, female_mortality: list, male_incidence: list, male_mortality: list
		"""
		female_incidence = []
		female_mortality = []
		male_incidence = []
		male_mortality = []
		for index in range(len(StatisticalTest.data_frame)):
			female_incidence.append(StatisticalTest.data_frame[StatisticalTest.female_incidence][index])
			female_mortality.append(StatisticalTest.data_frame[StatisticalTest.female_mortality][index])
			male_incidence.append(StatisticalTest.data_frame[StatisticalTest.male_incidence][index])
			male_mortality.append(StatisticalTest.data_frame[StatisticalTest.male_mortality][index])

		return female_incidence, female_mortality, male_incidence, male_mortality

	@staticmethod
	def calculate_ANOVA_test(values):
		"""
		# values: female_incidence, female_mortality, male_incidence, male_mortality
		calculates an ANOVA test to determine if there is a statistical difference between men and women's incidence/mortality rate of cancer
		:param values: values: tuple of lists
		:return: None
		"""

		# calculate incidence rate between males and females
		# null hypothesis: men and women have similar incidence/mortality rates

		incidence_statistic, incidence_p_value = stats.f_oneway(values[0], values[2])
		mortality_statistic, mortality_p_value = stats.f_oneway(values[1], values[3])

	@staticmethod
	def standardize_data(data_frame: pd.DataFrame):
		"""
			This function will standardize the data frame passed in
			standardize: a data set containing a mean of 0 and an standard deviation of 1
			Steps:
				1) Calculate mean of data set
				2) Calculate standard deviation of set
				3) Subtract mean from each value
				4) Divide the new value by the standard deviation

				(x - max) / (max - min)
			"""
		new_df = pd.DataFrame.copy(data_frame)
		standardized = np.array(stats.zscore(new_df))
		return standardized

	@staticmethod
	def box_plot_statistics(values: pd.DataFrame, state_names: pd.DataFrame, data_to_use: str):
		list_of_values = []  # create a nested list to correlate state name with value. Allows for sorting. [state_name, value]

		# incidence rate has Pennsylvania as an outlier, while mortality rate does not
		outlier_list = ['California', 'Florida', 'New York', 'Texas']
		if data_to_use == 'incidence_rate':
			outlier_list.append('Pennsylvania')

		# create nested list
		for i in range(len(values)):
			list_of_values.append([state_names[i], values[i]])

		# sort value from low to high
		list_of_values = sorted(list_of_values, key=lambda x: x[1])

		maximum = list_of_values[0][1]  # does not include outliers. Set first value to min/max for comparisons
		minimum = list_of_values[0][1]  # does not include outliers
		max_state = list_of_values[0][0]
		min_state = list_of_values[0][0]

		# find max and min
		for i in range(len(list_of_values)):
			if list_of_values[i][0] not in outlier_list:  # don't want to factor in outliers
				if list_of_values[i][1] > maximum:  # test for max
					maximum = list_of_values[i][1]
					max_state = list_of_values[i][0]
				elif list_of_values[i][1] < minimum:  # if not max, test for min
					minimum = list_of_values[i][1]
					min_state = list_of_values[i][0]

		# calculate quartile values
		q1_index = round((1/4) * (len(list_of_values) + 1))
		q2_index = round((1/2) * (len(list_of_values) + 1))
		q3_index = round((3/4) * (len(list_of_values) + 1))

		first_quartile = list_of_values[q1_index]
		second_quartile = list_of_values[q2_index]
		third_quartile = list_of_values[q3_index]
		interquartile_range = third_quartile[1] - first_quartile[1]
		mean = np.average(values)

		"""
		print('first_quartile: %s' % first_quartile)
		print('second_quartile: %s' % second_quartile)
		print('third_quartile: %s' % third_quartile)
		print('interquartile_range: %s' % interquartile_range)
		print('mean: %s' % mean)
		print('maximum: %s' % maximum)
		print('minimum: %s' % minimum)
		print('max_state: %s' % max_state)
		print('min_state: %s' % min_state)
		"""
