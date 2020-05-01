# t-test: is there a significant difference between the mean of two sets
# compare the mean between male and female incidence rates
# compare the mean between male and female mortality rates
# this can tell us if there was a significant difference in incidence/mortality rates between males and females
#       from 1999 to 2016

import numpy as np
import pandas as pd
from scipy import stats

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
		values = self.return_values()
		self.calculate_statistics(values)
		self.average_group_population()

	def return_values(self):

		female_incidence = []
		female_mortality = []
		male_incidence = []
		male_mortality = []
		for index in range(len(StatisticalTest.data_frame)):
			female_incidence.append(StatisticalTest.data_frame[StatisticalTest.female_incidence][index])  # female incidence
			female_mortality.append(StatisticalTest.data_frame[StatisticalTest.female_mortality][index])  # female mortality

			male_incidence.append(StatisticalTest.data_frame[StatisticalTest.male_incidence][index])     # male incidence
			male_mortality.append(StatisticalTest.data_frame[StatisticalTest.male_mortality][index])     # male mortality

		return female_incidence, female_mortality, male_incidence, male_mortality

	# values: female_incidence, female_mortality, male_incidence, male_mortality
	def calculate_statistics(self, values):

		# calculate incidence rate between males and females
		# null hypothesis: men and women have similar incidence rates
		# alternate hypothesis: incidence rates between men and women are different

		incidence_statistic, incidence_p_value = stats.ttest_rel(values[0], values[2])
		mortality_statistic, mortality_p_value = stats.ttest_rel(values[1], values[3])

		# print("Incidence statistic: %s" % incidence_statistic)
		# print("Incidence p value: %s" % incidence_p_value)
		# print("Mortality statistic: %s" % mortality_statistic)
		# print("Mortality p value: %s" % mortality_p_value)

	def average_group_population(self):
		female_incidence = 0
		female_mortality = 0
		male_incidence = 0
		male_mortality = 0

		for index in range(len(StatisticalTest.data_frame)):
			female_incidence += StatisticalTest.data_frame[StatisticalTest.female_incidence][index]
			female_mortality += StatisticalTest.data_frame[StatisticalTest.female_mortality][index]
			male_incidence += StatisticalTest.data_frame[StatisticalTest.male_incidence][index]
			male_mortality += StatisticalTest.data_frame[StatisticalTest.male_mortality][index]

		# print("female_incidence: %s" % female_incidence)
		# print("female_mortality: %s" % female_mortality)
		# print("male_incidence: %s" % male_incidence)
		# print("male_mortality: %s" % male_mortality)