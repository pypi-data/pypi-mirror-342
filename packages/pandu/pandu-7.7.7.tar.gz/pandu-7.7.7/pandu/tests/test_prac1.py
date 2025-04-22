import os

file_path = os.path.join(os.path.dirname(__file__), 'pandu', 'prac1', 'one.py')

with open(file_path, 'r') as f:
    print(f.read())
