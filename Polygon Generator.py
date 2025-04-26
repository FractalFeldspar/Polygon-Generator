import matplotlib.pyplot as plt
import numpy as np
from numpy import random
import math

numPoints = 20
xValues = [random.uniform(0,100) for _ in range(numPoints)]
yValues = [random.uniform(0,100) for _ in range(numPoints)]

minX = min(xValues)
maxX = max(xValues)
averageX = 0.5*(minX+maxX)
minY = min(yValues)
maxY = max(yValues)
averageY = 0.5*(minY+maxY)

# Calculate angle to the max X value point
maxXIndex = xValues.index(maxX)
yAtMaxX = yValues[maxXIndex]
maxXTheta = math.atan2(yAtMaxX-averageY, maxX-averageX)
print("maxXTheta: ", math.degrees(maxXTheta))
print(maxX)
print(yAtMaxX)

# Calculate angle to every point. Offset by angle to max X value point
points = []
for x, y in zip(xValues, yValues):
    adjustedX = x-averageX
    adjustedY = y-averageY
    theta = math.atan2(adjustedY, adjustedX)
    theta = theta-maxXTheta
    theta = theta % (2 * math.pi)  # Wrap to [0, 2pi)
    points.append((theta, x, y))

# Sort by wrapped theta
points.sort()

# Remove angle offset, convert to degrees
sorted_theta, sorted_x_tuple, sorted_y_tuple = zip(*points)
sorted_x = list(sorted_x_tuple)
sorted_y = list(sorted_y_tuple)
sorted_theta = [(t+maxXTheta) % (2 * math.pi) for t in sorted_theta]
sorted_theta = [math.degrees(t) for t in sorted_theta]

# print("Sorted x:", sorted_x)
# print("Sorted y:", sorted_y)
print("Sorted theta:", sorted_theta)


# sorted_x.append(maxX)
# sorted_y.append(yAtMaxX)
sorted_x.extend(sorted_x[0:2])
sorted_y.extend(sorted_y[0:2])
print("Sorted x:", sorted_x)
print("Sorted y:", sorted_y)
polygon_indexes = [0]
i = 0
j = 0
while i+j < len(sorted_x)-2:
    vector_1 = np.array([sorted_x[i+j+1]-sorted_x[i], sorted_y[i+j+1]-sorted_y[i], 0])
    vector_2 = np.array([sorted_x[i+j+2]-sorted_x[i], sorted_y[i+j+2]-sorted_y[i], 0])
    # Find locally convex points
    if np.cross(vector_1, vector_2)[2] > 0:
        polygon_indexes.append(i+j+1)
        i = i+j+1
        j = 0
        # If you find any points that would make the polygon become concave, perform a binary search through previously added polygon points
        if i>0:
            vector_previous = np.array([sorted_x[i]-sorted_x[polygon_indexes[-2]], sorted_y[i]-sorted_y[polygon_indexes[-2]], 0])
        else:
            vector_previous = np.array([0, 1, 0])
        if np.cross(vector_1, vector_previous)[2] >= 0:
            polygon_search_index_lower_bound = 0
            polygon_search_index_upper_bound = len(polygon_indexes)-1
            critical_point_found = False
            while not critical_point_found:
                polygon_search_index = (polygon_search_index_lower_bound+polygon_search_index_upper_bound)//2
                point_search_index = polygon_indexes[polygon_search_index]
                forward_point_search_index = polygon_indexes[polygon_search_index+1]
                backward_point_search_index = polygon_indexes[polygon_search_index-1]
                search_vector = np.array([sorted_x[point_search_index]-sorted_x[i], sorted_y[point_search_index]-sorted_y[i], 0])
                forward_vector = np.array([sorted_x[forward_point_search_index]-sorted_x[i], sorted_y[forward_point_search_index]-sorted_y[i], 0])
                backward_vector = np.array([sorted_x[backward_point_search_index]-sorted_x[i], sorted_y[backward_point_search_index]-sorted_y[i], 0])
                if np.cross(search_vector, forward_vector)[2] > 0: # need to move search vector forward
                    polygon_search_index_lower_bound = polygon_search_index
                elif np.cross(search_vector, backward_vector)[2] > 0: # need to move search vector backward
                    polygon_search_index_upper_bound = polygon_search_index
                else:
                    critical_point_found = True
                    print("polygon search index", polygon_search_index)
                    print("pre deletion:", polygon_indexes)
                    del polygon_indexes[polygon_search_index+1:-1]
                    print("post deletion:", polygon_indexes)
    else:
        j = j+1

# polygon_indexes.append(0)
print(polygon_indexes)

polygon_x = [sorted_x[index] for index in polygon_indexes]
polygon_y = [sorted_y[index] for index in polygon_indexes]

print(polygon_x)
print(polygon_y)

plt.plot(xValues, yValues, 'o')
plt.plot(averageX, averageY, 'om')
plt.plot(polygon_x, polygon_y, 'c')
# plt.plot(new_polygon_x, new_polygon_y, ':k')
plt.show()