import time

def square(x):
    return x**2

def double(x):
    return x * 2

nums = [1,2,3,4,5]

def num_cal(data, fun):
    start_time = time.time()
    print([fun(x) for x in data])
    end_time = time.time()
    print(end_time - start_time)

num_cal(nums, square)
num_cal(nums, double)