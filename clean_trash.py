import argparse
import os
import fnmatch
import time

#C:\Users\Cyber Kanojo\Desktop\programming\Levashov_Maxim_python2023\trash_folder

parser = argparse.ArgumentParser(description="Trash script")
parser.add_argument("--trash_folder_path", help="Path to the file", type = str, required = True)
parser.add_argument("--age_thr", help = "Time to delete", type = int, required = True)

args = parser.parse_args()

path = args.trash_folder_path
input_time = args.age_thr
current_time = time.time()

for root , directory , file in os.walk(path):
    for filename in file:
        path = os.path.join(root, filename)
        file_time = os.path.getmtime(path)
        print(file_time)
        if (current_time - file_time) > input_time:
            print(f"Deleting: {path}")
            os.remove(path)

