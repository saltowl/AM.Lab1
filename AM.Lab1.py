import matplotlib.pyplot as plt
import math

def get_input_data(file_name):
	with open(file_name, "r") as file:
		input_data = []
		for line in file:
			try:
				input_data += map(float, line.replace(",", ".").split())
			except ValueError: #if not numbers in line
				pass
	return input_data


def calculate_probability(data):
	return {value : data.count(value)/len(data) for value in data}


def get_minimum(data):
	return min(data)


def get_maximum(data):
	return max(data)


def plot_histogram(data):
	count = math.ceil(len(data)**(1/3)) # count of intervals
	begin = math.floor(get_minimum(data))
	end = math.ceil(get_maximum(data))
	step = round((end - begin) / count) # width of interval
	x = []
	y = []
	xi = begin
	i = 0

	while i < count:
		count_in_one_interval = 0
		
		for item in data:
			if (((item < xi + step) & (item > xi) & (xi != begin) & (xi != end)) 
                | ((xi == begin) & (item < xi + step)) 
                | ((xi == end) & (item > xi))):
				count_in_one_interval +=1
		
		probability = count_in_one_interval / len(data)
		
		x.append(xi)
		y.append(probability / step)
		i += 1
		xi += step
	
	plt.style.use("bmh")
	plt.bar(x, y, step, align = 'edge', color = 'sandybrown', edgecolor = 'sienna', linewidth = 1.5)
	plt.xlabel("Values")
	plt.ylabel("Probability / Width of interval")
	plt.title("Histogram")
	pass


def plot_distr_func(data):

	def plot_hor_line(begin, end, y):
		hor_line = {"x" : [begin, end], "y" : [y, y]}
		plt.plot(hor_line["x"], hor_line["y"], color="black", linestyle="solid", linewidth=1)
		pass
	
	def plot_ver_line(x, end, begin=0):
		ver_line = {"x" : [x, x], "y" : [begin, end]}
		plt.plot(ver_line["x"], ver_line["y"], color="black", linestyle="dashed", linewidth=0.8)


	data_prob = calculate_probability(data)

	prob_sum = 0
	previous_value = 0
	for value in sorted(data_prob.keys()):
		plot_hor_line(previous_value, value, prob_sum)
		previous_value = value

		prob_sum += data_prob[value]
		prob_sum = round(prob_sum, len(str(len(data))) - 1)
		plot_ver_line(value, prob_sum)
	plot_hor_line(previous_value, previous_value + 1, prob_sum)
	pass


def print_statistic(data):
	mean_value = calculate_mean_value(data)
	sample_variance = calculate_sample_variance(data)
	modus = calculate_modus(data)
	standart_error = calculate_standart_error(data)
	median = calculate_median(data)
	quartiles = calculate_quartiles(data)
	standard_deviation = calculate_standard_deviation(data)

	print("Mean: {:.2f}".format(mean_value))
	print("Sample variance: {:.2f}".format(sample_variance))
	print("Standart Error: {:.2f}".format(standart_error))
	print("Modus: {:.2f}".format(modus))
	print("Median: {:.2f}".format(median))
	print("First quartile (0.25 quantile): {:.2f}".format(quartiles[0]))
	print("Second quartile (0.5 quantile): {:.2f}".format(quartiles[1]))
	print("Third quartile (0.75 quantile): {:.2f}".format(quartiles[2]))
	print("Standard deviation: {:.2f}".format(standard_deviation))

	pass


def main():
	input_data = get_input_data("input.txt")

	plot_histogram(input_data)
	plt.show()
	plot_distr_func(input_data)
	plt.show()

	print_statistic(input_data)
	pass


def calculate_mean_value(data):
	return sum(data)/len(data)


def calculate_sample_variance(data):
	sum = 0
	mean_value = calculate_mean_value(data)
	for item in data:
		sum += (item - mean_value)**2
	return sum / len(data)


def calculate_modus(data):
	sorted_data = sorted(calculate_probability(data).items(), key=lambda x: x[1])
	return sorted_data[-1][0]


def calculate_standart_error(data):
	return math.sqrt(calculate_sample_variance(data)/len(data))


def calculate_quartiles(data):
	sorted_data = sorted(data)
	middle_index = len(data) // 2

	first_quartile = calculate_median(sorted_data[:middle_index])
	second_quartile = calculate_median(data)
	third_quartile = calculate_median(sorted_data[middle_index:])

	return [first_quartile, second_quartile, third_quartile]


def calculate_standard_deviation(data):
	return math.sqrt(calculate_sample_variance(data))


def calculate_median(data):
	sorted_data = sorted(data)
	middle_index = len(data) // 2

	median = 0
	if middle_index % 2 == 0:
		median = (sorted_data[middle_index - 1] + sorted_data[middle_index]) / 2
	else:
		median = sorted_data[middle_index]

	return median


main()
