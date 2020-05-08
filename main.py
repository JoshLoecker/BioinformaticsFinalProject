from DataFrame import DataFrame
from PlotGeneration import PlotGeneration
from LoadData import load_data
from StatisticalTest import StatisticalTest

if __name__ == "__main__":

	print("Loading data frames. . .")
	load_data()                       # load data

	print("Loading statistics. . .")
	DataFrame.FemaleIncidenceRate()         # generate female incidence rates
	DataFrame.FemaleMortalityRate()         # generate female mortality rates
	DataFrame.MaleIncidenceRate()           # generate male incidence rates
	DataFrame.MaleMortalityRate()           # generate male morality rates

	print("Generating CSV file. . .")
	PlotGeneration.create_csv()             # generate the CSV file to create the map

	print("Generating map. . .")
	PlotGeneration.generate_choropleth()    # map creation
	PlotGeneration.generate_sankey()        # sankey plot generation
	PlotGeneration.generate_boxplot()

	print("Calculating statistics. . .")    # T-Test generation, calculating averages
	StatisticalTest()
