import argparse
import os
import fnmatch

def git_ignored_path(project_dir):
    gitignore_path = os.path.join(project_dir, '.gitignore')
    with open(gitignore_path, "r") as data: #с помощью with файл сразу закроется
        ignored_types = []
        for line in data:
            line = line.strip() #избавляемся от всяких там \n
            if not line or line.startswith('#'): #скипаем комментарии и пустые строки
                continue
            if line[0] == '/':
                line = line[1:]
            ignored_types.append(line)
        return ignored_types

def ignored_regex(ignored_types):
    regex_types = []
    for i in range(len(ignored_types)):
        element = ignored_types[i]
        if (element[0] == '*'):
            regex_types.append(element)
    return regex_types

parser = argparse.ArgumentParser(description="Directory ignored files")
parser.add_argument("--project_dir", help="Path to the file", type = str, required = True)

args = parser.parse_args()
#print(args.project_dir)
#print(list(os.listdir(args.project_dir)))
#print(git_ignored_path(args.project_dir))
ignored_regex(git_ignored_path(args.project_dir))

check_array = git_ignored_path(args.project_dir)
regex_check_array = ignored_regex(check_array)

print("Ignored files")


for root, dirs, files in os.walk(args.project_dir):
    for file in files:
        if file in check_array:
            print(f"{os.path.join(root,file)} ignored by expression {file}")
            continue

        for pattern in regex_check_array:
            if fnmatch.fnmatch(file, pattern):
                print(f"{os.path.join(root,file)} ignored by expression {pattern}")
                break