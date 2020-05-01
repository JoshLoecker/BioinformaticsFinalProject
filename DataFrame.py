class DataFrame:
	"""
	Global variables for the class
	"""

	data_file = r"statistics/BYAREA.TXT"  # data file for instance/moratlity rates for the US
	class_instances = []                  # this will hold the DataFrame instance
	female_incidence = []                 # this will hold the DataFrame instances that relate to female incidence
	female_mortality = []                 # this will hold the DataFrame instances that relate to female mortality
	male_incidence = []                   # this will hold the DataFrame instances that relate to male incidence
	male_mortality = []                   # this will hold the DataFrame instances that relate to male mortality
	state_list = []                       # this will only hold state names

	"""
	these are the attributes in the data file
	"""
	# AREA
	# AGE_ADJUSTED_CI_LOWER
	# AGE_ADJUSTED_CI_UPPER
	# AGE_ADJUSTED_RATE
	# COUNT
	# EVENT_TYPE
	# POPULATION
	# RACE
	# SEX
	# SITE
	# YEAR
	# CRUDE_CI_LOWER
	# CRUDE_CI_UPPER
	# CRUDE_RATE

	# init function for storing data about each row in the BYAREA.txt file
	def __init__(self, area, age_adjusted_ci_lower, age_adjusted_ci_upper, age_adjusted_rate,
	             count, event_type, population, race, sex, site, year, crude_ci_lower, crude_ci_upper, crude_rate):
		self.AREA = area
		self.AGE_ADJUSTED_CI_LOWER = age_adjusted_ci_lower
		self.AGE_ADJUSTED_CI_UPPER = age_adjusted_ci_upper
		self.AGE_ADJUSTED_RATE = age_adjusted_rate
		self.COUNT = count
		self.EVENT_TYPE = event_type
		self.POPULATION = population
		self.RACE = race
		self.SEX = sex
		self.SITE = site
		self.YEAR = year
		self.CRUDE_CI_LOWER = crude_ci_lower
		self.CRUDE_CI_UPPER = crude_ci_upper
		self.CRUDE_RATE = crude_rate

	# this will parse the female incidence rates and load them into the DataFrame.female_incidence list
	@staticmethod
	def FemaleIncidenceRate():



		# temporary list for holding instances containing only U.S. state names
		female_incidence = []
		for instance in DataFrame.class_instances:
			# All female incidence
			# the area in double quotes filters what we are looking for
			if instance.SEX.lower() == "female":
				if instance.RACE.lower() == "all races":
					if instance.SITE.lower() == "all cancer sites combined":
						if instance.YEAR == "2012-2016":
							if instance.EVENT_TYPE.lower() == "incidence":
								female_incidence.append(instance)

		# remove incidences that are outside states in the U.S. (i.e. Puerto Rico)
		for frame in female_incidence:              # filter through all female DataFrames
			for state in DataFrame.state_list:                # iterate through state names
				if frame.AREA.lower() == state.lower():       # if DataFrame state name matches state list name
					DataFrame.female_incidence.append(frame)
					break                                     # go to next DataFrame item

	# this will parse the female incidence rates and load them into the DataFrame.female_mortality list
	@staticmethod
	def FemaleMortalityRate():
		# temporary list for holding instances containing only U.S. state names
		female_mortality = []
		for instance in DataFrame.class_instances:
			# All female incidence
			# the area in double quotes filters what we are looking for
			if instance.SEX.lower() == "female":
				if instance.RACE.lower() == "all races":
					if instance.SITE.lower() == "all cancer sites combined":
						if instance.YEAR == "2012-2016":
							if instance.EVENT_TYPE.lower() == "mortality":
								female_mortality.append(instance)

		# remove incidences that are outside states in the U.S. (i.e. Puerto Rico)
		for frame in female_mortality:  # filter through all female DataFrames
			for state in DataFrame.state_list:  # iterate through state names
				if frame.AREA.lower() == state.lower():  # if DataFrame state name matches state list name
					DataFrame.female_mortality.append(frame)
					break  # go to next DataFrame item

	# This method follows the same outline as FemaleIncidenceRate, but for male incidence rates
	# This will keep results in the DataFrame.male_incidence list
	@staticmethod
	def MaleIncidenceRate():
		male_incidence = []
		for incidence in DataFrame.class_instances:
			# All male incidence
			if incidence.SEX.lower() == "male":
				if incidence.RACE.lower() == "all races":
					if incidence.SITE.lower() == "all cancer sites combined":
						if incidence.YEAR == "2012-2016":
							if incidence.EVENT_TYPE.lower() == "incidence":
								male_incidence.append(incidence)

		for frame in male_incidence:
			for state in DataFrame.state_list:
				if frame.AREA.lower() == state.lower():
					DataFrame.male_incidence.append(frame)
					break

	# This method follows the same outline as FemaleMortalityRate, but for male mortality rates
	# This will keep results in the DataFrame.male_mortality list
	@staticmethod
	def MaleMortalityRate():
		male_mortality = []
		for mortality in DataFrame.class_instances:
			# All male incidence
			if mortality.SEX.lower() == "male":
				if mortality.RACE.lower() == "all races":
					if mortality.SITE.lower() == "all cancer sites combined":
						if mortality.YEAR == "2012-2016":
							if mortality.EVENT_TYPE.lower() == "mortality":
								male_mortality.append(mortality)

		for frame in male_mortality:
			for state in DataFrame.state_list:
				if frame.AREA.lower() == state.lower():
					DataFrame.male_mortality.append(frame)
					break

	# this provides a more simple method of printing DataFrame instances, used mostly in debugging
	@staticmethod
	def PrintInstance(frame, attribute):
		"""available attribute options are: area, count, event, population, race, sex, site, year"""
		if attribute.lower() == "all":
			print("Area: %s" % frame.area)
			print("Count: %s" % frame.count)
			print("Event Type: %s" % frame.event_type)
			print("Population: %s" % frame.population)
			print("Race: %s" % frame.race)
			print("Sex: %s" % frame.sex)
			print("Site: %s" % frame.site)
			print("Year: %s" % frame.year)
		elif attribute.lower() == "area":
			print("Area: %s" % frame.area)
		elif attribute.lower() == "count":
			print("Count: %s" % frame.count)
		elif attribute.lower() == "event":
			print("Event: %s" % frame.event_type)
		elif attribute.lower() == "population":
			print("Population: %s" % frame.population)
		elif attribute.lower() == "race":
			print("Race: %s" % frame.race)
		elif attribute.lower() == "sex":
			print("Sex: %s" % frame.sex)
		elif attribute.lower() == "site":
			print("Site: %s" % frame.site)
		elif attribute.lower() == "year":
			print("Year: %s" % frame.year)
