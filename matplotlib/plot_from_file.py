import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('data.csv', dtype={'names': ('r', 'p', 'success_rate'), 'formats': (np.int, np.float, np.float)}, delimiter=',', skiprows=1)

colors = ['red', 'orange', 'green', 'blue', 'purple']
p_values = np.arange(0.01, 0.21, 0.01)

for i in range(2, 7):
	selected_data = data[data['r'] == i]
	print(i)
	plt.plot(p_values, selected_data['success_rate'], colors[i-2])


plt.title('Hamming coding success rate')
plt.xlabel('Error rate p')
plt.ylabel('Success rate')
plt.show()