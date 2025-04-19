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
            ignored_types.append(line)
        return ignored_types

def ignored_regex(ignored_types):
    regex_types = [[],[]]
    for i in range(len(ignored_types)):
        element = ignored_types[i]
        if (element[0] == '*'):
            regex_types[0].append(element)
            regex_types[1].append(len(element))
    return regex_types

parser = argparse.ArgumentParser(description="Directory ignored files")
parser.add_argument("--project_dir", help="Path to the file", type = str, required = True)

args = parser.parse_args()
print(args.project_dir)
print(list(os.listdir(args.project_dir)))
print(git_ignored_path(args.project_dir))
ignored_regex(git_ignored_path(args.project_dir))