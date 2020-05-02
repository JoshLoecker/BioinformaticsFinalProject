from DataFrame import DataFrame
from MapGeneration import MapGeneration
from LoadData import load_data
from StatisticalTest import StatisticalTest

if __name__ == "__main__":

	print("Loading data frames. . .")
	load_data()                       # load data

	print("Loading statistics. . .")
	DataFrame.FemaleIncidenceRate()  # generate female incidence rates
	DataFrame.FemaleMortalityRate()  # generate female mortality rates
	DataFrame.MaleIncidenceRate()    # generate male incidence rates
	DataFrame.MaleMortalityRate()    # generate male morality rates

	print("Generating CSV file. . .")
	MapGeneration.create_csv()       # generate the CSV file to create the map

	print("Generating map. . .")
	MapGeneration.generate_map()     # map creation

	print("Calculating statistics. . .")
	StatisticalTest()
