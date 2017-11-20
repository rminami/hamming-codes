import matplotlib.pyplot as plt
import numpy as np
import sys

def main(args):

	min = 0
	max = 1
	inc = 0.01

	for arg in args:
		if arg == '-u':
			print('min: ', end='')
			min = float(input())

			print('max: ', end='')
			max = float(input())

			print('inc: ', end='')
			inc = float(input())		

	p_values = np.arange(min, np.nextafter(max, 2), inc)
	colors = ['red', 'orange', 'green', 'blue', 'purple']
	# colors = ['#0caadc', '#11b5e4', '#1481ba', '#034748', '#001021']

	for r in range(6, 1, -1):
		n = 2 ** r - 1
		rdata = []
		for p in p_values:
			rdata.append((1 - p) ** n + n * p * (1 - p) ** (n - 1))
		
		plt.plot(p_values, rdata, colors[r-2], label='r='+str(r))

	plt.title('Hamming coding success rate')
	plt.xlabel('Error rate p')
	plt.ylabel('Success rate')
	plt.legend()
	plt.show()

if __name__ == '__main__':
	main(sys.argv[1:])