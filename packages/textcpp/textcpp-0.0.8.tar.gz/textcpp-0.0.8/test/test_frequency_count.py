from textcpp import text_utils
import time
from collections import Counter
import string


def frequency_count_py(path):
    word_freq = Counter()
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            # Remove punctuation and convert to lowercase
            line = line.translate(str.maketrans("", "", string.punctuation)).lower()
            words = line.split()
            word_freq.update(words)
    return dict(word_freq)


file_path = "test/shakespeare.txt"

# Benchmark C++
start = time.time()
freq_cpp = text_utils.frequency_count(file_path)
end = time.time()
execution_cpp_time = end - start
print(f"C++ runtime: {execution_cpp_time:.4f} seconds")

# Benchmark Python
start = time.time()
freq_py = frequency_count_py(file_path)
end = time.time()
execution_py_time = end - start
print(f"Python runtime: {execution_py_time:.4f} seconds")

print(f"Same result? {freq_cpp == freq_py}")
print(len(freq_cpp), len(freq_py))
