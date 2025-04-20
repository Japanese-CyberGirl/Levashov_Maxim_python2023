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
#current_time = time.time()

log_file = open("clean_trash.log", "a")


while(True):
    current_time = time.time()
    #удаление обычных файлов
    for root , directory , file in os.walk(path):
        for filename in file:
            file_path = os.path.join(root, filename)
            file_time = os.path.getmtime(file_path)
            print(file_time)
            if (current_time - file_time) > input_time:
                print(f"Deleting: {file_path}")
                os.remove(file_path)
                log_file.write(f"Removed file: {file_path}\n")
                log_file.flush() #принудительно записываем информацию в логи


    for root, directory, file in os.walk(path, topdown = False): #удаление пустых папок, начиная с конца, а не с родительских
        for directory_name in directory:
            directory_path = os.path.join(root, directory_name)
            if not os.listdir(directory_path): #если папка пустая, то удаляем...
                os.rmdir(directory_path)
                log_file.write(f"Removed empty directory {directory_path}\n")
                log_file.flush()

    time.sleep(1)
