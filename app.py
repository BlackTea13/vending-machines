import sys
import numpy as np

file_name = sys.argv[1]

with open(file_name, 'r') as file:
    contents = file.read()
    numbers = []
    for i in contents:
        if i.isdigit():
            numbers.append(int(i))

    numbers = np.array(numbers)
    print(f"Statistics Summary")
    print(f"mean: {np.mean(numbers)}")
    print(f"std: {np.std(numbers)}")
    print(f"min: {np.min(numbers)}")
    print(f"max: {np.max(numbers)}")
