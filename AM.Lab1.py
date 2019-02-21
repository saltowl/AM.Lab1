import matplotlib.pyplot as plt


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


def main():
	input_data = get_input_data("input.txt")

	plot_distr_func(input_data)
	plt.show()
	pass

main()
