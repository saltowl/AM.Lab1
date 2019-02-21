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

def print_histogram(data):
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

	plt.show()
	pass

def main():
	input_data = get_input_data("input.txt")

	pass

main()
