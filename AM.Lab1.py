import matplotlib.pyplot as plt
import scipy.stats as st
import math
from Interval import Interval

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


def calculate_intervals(data):
	begin = math.floor(get_minimum(data))
	end = math.ceil(get_maximum(data))
	step = round((end - begin)**(1/3)) # width of interval
	count = round((end - begin) / step) # count of intervals
	
	intervals = [Interval() for i in range(count)]
	current_border = begin
	for interval in intervals:
		interval.begin = current_border
		interval.end = current_border + step
		current_border += step

	for value in data:
		current_interval = intervals[int(value / step)]
		current_interval.count += 1
		current_interval.sum = round(current_interval.sum, 1) + value

	for interval in intervals:
		interval.probability = interval.count / (len(data) * step)
		interval.mean = round(interval.sum / interval.count, 1)

	return intervals


def plot_histogram(data):
	plt.figure()

	intervals = calculate_intervals(data)
	left_borders = [interval.begin for interval in intervals]
	probabilities = [interval.probability for interval in intervals]
	step = left_borders[1] - left_borders[0]
	
	plt.style.use("bmh")
	plt.bar(left_borders, probabilities, step, align = 'edge', color = 'sandybrown', edgecolor = 'sienna', linewidth = 1.5)
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
	conf_interval_E = calculate_conf_interval_E(data, 0.95)
	conf_interval_S = calculate_conf_interval_S(data, 0.95)

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

	print("\nConfidence interval for mathematical expectation: ({:.2f}; {:.2f})"
	   .format(conf_interval_E[0], conf_interval_E[1]))
	print("Confidence interval for standard deviation: ({:.2f}; {:.2f})"
	   .format(conf_interval_S[0], conf_interval_S[1]))

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
	data_prob = calculate_probability(data)

	mean_value = 0
	for value in data_prob:
		mean_value += value * data_prob[value]

	return mean_value


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
	mean_value = calculate_mean_value(data)

	central_moment = 0
	for value in data_prob:
		central_moment += data_prob[value] * (value - mean_value)**rank

	return central_moment


def calculate_median(data):
	sorted_data = sorted(data)
	middle_index = len(data) // 2

	median = 0
	if middle_index % 2 == 0:
		median = (sorted_data[middle_index - 1] + sorted_data[middle_index]) / 2
	else:
		median = sorted_data[middle_index]

	return median


def calculate_conf_interval_E(data, gamma):
	return st.t.interval(gamma, len(data) - 1, calculate_mean_value(data))


def calculate_conf_interval_S(data, gamma):
	df = len(data) - 1
	chi2_k1 = st.chi2.ppf((1 + gamma) / 2, df)
	chi2_k2 = st.chi2.ppf((1 - gamma) / 2, df)
	S = calculate_standard_deviation(data)

	return (S * ((df / chi2_k1)**(1/2)), S * ((df / chi2_k2)**(1/2)))


main()
