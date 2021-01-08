import os

cur_path = os.path.dirname(__file__)
print(cur_path)
new_path = os.path.join(cur_path,'input', 'boundary.txt')
print(new_path)
file1 = open(new_path, "r+")
text = file1.readlines()
print(text)