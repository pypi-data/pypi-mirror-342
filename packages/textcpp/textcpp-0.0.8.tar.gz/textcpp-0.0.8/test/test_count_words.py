from textcpp import text_utils
import time


start = time.time()
len_text_cpp = text_utils.count_words("test/shakespeare.txt")
end = time.time()
execution_cpp_time = end-start
print(f"cpp runtime {execution_cpp_time}")

start = time.time()
with open("test/shakespeare.txt", "r") as f:
    text = f.read()
len_text_python = len(text.split())
end = time.time()
execution_python_time = end-start
print(f"python runtime {execution_python_time}")

print(len_text_cpp ==len_text_python )