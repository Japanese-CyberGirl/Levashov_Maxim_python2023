import argparse
import os

parser = argparse.ArgumentParser(description="Directory ignored files")
parser.add_argument("--project_dir", help="Path to the file", type = str, required = True)

args = parser.parse_args()
print(args.project_dir)
print(list(os.listdir(args.project_dir)))
