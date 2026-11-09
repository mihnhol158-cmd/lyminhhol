import time

# Create sorted list
numbers = list(range(1000000))

target = 999999

# Linear Search
start = time.perf_counter()

linear_search(numbers, target)

end = time.perf_counter()

linear_time = end - start


# Binary Search
start = time.perf_counter()

binary_search(numbers, target)

end = time.perf_counter()

binary_time = end - start


# Display results
print("Linear Search:", linear_time, "seconds")
print("Binary Search:", binary_time, "seconds")