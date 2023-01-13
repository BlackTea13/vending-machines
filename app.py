import sys
import numpy as np

# file_name = sys.argv[1]

print(f"Statistics Summary")
total_numbers = []
for file_name in sys.argv[1:]:
    with open(file_name, 'r') as file:
        contents = file.read()
        numbers = []
        for i in contents:
            if i.isdigit():
                numbers.append(int(i))
                total_numbers.append(int(i))

        numbers = np.array(numbers)
        print(file_name)
        print(f"mean: {np.mean(numbers)} std: {np.std(numbers)} min: {np.min(numbers)} max: {np.max(numbers)} n: {len(numbers)}")
        # print(f"mean: {np.mean(numbers)}")
        # print(f"std: {np.std(numbers)}")
        # print(f"min: {np.min(numbers)}")
        # print(f"max: {np.max(numbers)}")

total_numbers = np.array(numbers)
print(f"combined")
print(f"mean: {np.mean(total_numbers)} std: {np.std(total_numbers)} min: {np.min(total_numbers)} max: {np.max(total_numbers)} n: {len(total_numbers)}")
