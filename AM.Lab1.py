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
	plt.figure()

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


	plt.figure()

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

	plt.title("Distribution function")
	plt.xlabel("x")
	plt.ylabel("F(x)")
	pass


def plot_mustached_box(data):
	plt.figure()

	min_value = get_minimum(data)
	max_value = get_maximum(data)
	quartiles = calculate_quartiles(data)

	plt.boxplot(data, vert=False)

	text_y = 0.89
	plt.text(min_value, text_y, "Min")
	plt.text(quartiles[0], text_y, "Q1")
	plt.text(quartiles[1], text_y, "Median")
	plt.text(quartiles[2], text_y, "Q3")
	plt.text(max_value, text_y, "Max")
	pass


def print_statistic(data):
	mean_value = calculate_mean_value(data)
	sample_variance = calculate_sample_variance(data)
	modus = calculate_modus(data)
	standart_error = calculate_standart_error(data)
	median = calculate_median(data)
	quartiles = calculate_quartiles(data)
	standard_deviation = calculate_standard_deviation(data)
	excess = calculate_excess(data)
	asymmetry = calculate_asymmetry(data)
	min_value = get_minimum(data)
	max_value = get_maximum(data)

	print("Mean: {:.2f}".format(mean_value))
	print("Sample variance: {:.2f}".format(sample_variance))
	print("Standart Error: {:.2f}".format(standart_error))
	print("Modus: {:.2f}".format(modus))
	print("Median: {:.2f}".format(median))
	print("First quartile (0.25 quantile): {:.2f}".format(quartiles[0]))
	print("Second quartile (0.5 quantile): {:.2f}".format(quartiles[1]))
	print("Third quartile (0.75 quantile): {:.2f}".format(quartiles[2]))
	print("Mustached Box parameters: {:.2f}|---{:.2f}|{:.2f}|{:.2f}---|{:.2f}"
	   .format(min_value, quartiles[0], quartiles[1], quartiles[2], max_value))
	print("Standard deviation: {:.2f}".format(standard_deviation))
	print("Excess: {:.2f}".format(excess))
	print("Asymmetry index: {:.2f}".format(asymmetry))
	print("Min: {:.2f}".format(min_value))
	print("Max: {:.2f}".format(max_value))

	pass


def main():
	input_data = get_input_data("input.txt")

	plot_histogram(input_data)
	plot_distr_func(input_data)
	plot_mustached_box(input_data)

	print_statistic(input_data)

	plt.show()
	pass


def calculate_mean_value(data):
	return sum(data)/len(data)


def calculate_sample_variance(data):
	return calculate_central_moment(data, 2)


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


def calculate_excess(data):
	return calculate_central_moment(data, 4) / (calculate_standard_deviation(data)**4) - 3


def calculate_asymmetry(data):
	return calculate_central_moment(data, 3) / (calculate_standard_deviation(data)**3)


def calculate_central_moment(data, rank):
	data_prob = calculate_probability(data)
	expected_value = calculate_expected_value(data)

	central_moment = 0
	for value in data_prob:
		central_moment += data_prob[value] * (value - expected_value)**rank

	return central_moment


def calculate_expected_value(data):
	data_prob = calculate_probability(data)

	expected_value = 0
	for value in data_prob:
		expected_value += value * data_prob[value]
	
	return expected_value


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
