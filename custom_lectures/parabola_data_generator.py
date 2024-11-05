import random

# Generate data to be curve fitted with a prabola

# Minimum and maximum x-values for the points to be generated between
min_x = 0
max_x = 10

# number of points to generate
num_points = 25

# uncertainty for the y value of each point
y_deviation = 20

# quadratic constants
a = 2.5
b = -1
c = 5

def quadratic(x):
    return a * x * x + b * x + c

def main():
    x_vals = [random.uniform(min_x, max_x) for _ in range(num_points)]
    x_vals.sort()
    y_vals = [quadratic(x_vals[i]) + random.uniform(-y_deviation, y_deviation) for i in range(num_points)]
    combined_points = [(x_vals[i], y_vals[i]) for i in range(num_points)]
    print(combined_points)
    
if __name__ == '__main__':
    main()
