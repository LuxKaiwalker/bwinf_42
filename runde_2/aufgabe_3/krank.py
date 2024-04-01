#dtatenstrukturen: koordinaten! dann kann man alles über analytische Geometrie machen.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

file = open("siedler2.txt", "r")
content = file.readlines()
file.close()
x = int(content[0]) #(anzahl der polygone)
land = []
lad = np.zeros((2, x), dtype = "float")
#kreis

land=[[float(value) for value in item.split()] for item in content[1:]]
x_coordinates, y_coordinates = zip(*land)

print(land)
# Create a Polygon patch
polygon = Polygon(land, closed=True, edgecolor='blue', facecolor='none')

# Create a figure and axis
fig, ax = plt.subplots()

# Add the Polygon patch to the axis
ax.add_patch(polygon)

# Plot the points
ax.scatter(x_coordinates, y_coordinates, color='red')

# Add labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_title('Polygon from Points')

# Show the plot
plt.show()
