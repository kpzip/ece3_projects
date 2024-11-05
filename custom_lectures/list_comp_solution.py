
x = [1 , 3 , 5 , 6]

y = [12 , 1 , 0 , 2]

z = [(x[i] + y[i]) for i in range(0, len(x)) if (x[i] + y[i]) > 5]

print(z)