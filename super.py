import os
import stat
import time
import argparse

today = int(time.time())
current_dir = os.getcwd()

def colored(text, color="white"):
    colors = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
    }

    if color.lower() not in colors:
        print(text) 
    else:
        print(colors[color.lower()] + text + colors["reset"])

def file_permissions(mode):
    is_dir = 'd' if stat.S_ISDIR(mode) else '-'
    perm = [
        (mode & stat.S_IRUSR) and 'r' or '-',
        (mode & stat.S_IWUSR) and 'w' or '-',
        (mode & stat.S_IXUSR) and 'x' or '-',
        (mode & stat.S_IRGRP) and 'r' or '-',
        (mode & stat.S_IWGRP) and 'w' or '-',
        (mode & stat.S_IXGRP) and 'x' or '-',
        (mode & stat.S_IROTH) and 'r' or '-',
        (mode & stat.S_IWOTH) and 'w' or '-',
        (mode & stat.S_IXOTH) and 'x' or '-',
    ]
    return is_dir + ''.join(perm)

def numeric_permissions(mode):
    user = (mode & stat.S_IRWXU) >> 6
    group = (mode & stat.S_IRWXG) >> 3
    others = (mode & stat.S_IRWXO)
    return f"{user}{group}{others}"

def save_file_perms(info):
    filename = f"{current_dir.replace('/', '-')}-{today}"
    try:
        for entry in os.scandir(current_dir):
            if entry.is_file() or entry.is_dir():
                stats = entry.stat()
                numeric_perm = numeric_permissions(stats.st_mode)
                
                if info:
                    print(f"{numeric_perm} {entry.name}")

                with open(f"{filename}.txt", "a") as f:
                    f.write(f"{numeric_perm} {entry.name}")
                    f.write('\n')
        print()
        colored(f"Saved to: {filename}.txt", "green")

    except Exception as e:
        colored(f"Something went wrong: {e}", "red")

def revert_file_perms(file):
    print()
    try:
        with open(file, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            perm_str, filename = line.strip().split(' ')
            perm = int(perm_str, 8) 

            filepath = os.path.join(current_dir, filename)
            if os.path.exists(filepath):
                os.chmod(filepath, perm)
                colored(f"Set {filename} to {perm_str}", "green")
            else:
                colored(f"File {filename} does not exist in the current directory.", "red")

    except Exception as e:
        colored(f"Something went wrong while reverting permissions: {e}", "red")


def find_file_perms():
    current_dir = os.getcwd()
    current_dir_hyphens = current_dir.replace('/', '-')
    files = []
    dir_files = []
    
    print("Finding files... \n")

    for entry in os.scandir(current_dir):
        if entry.is_file() and entry.name.startswith(current_dir_hyphens):
            file_timestamp = int(entry.name.split('-')[-1].split('.')[0])
            file_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_timestamp))
            files.append((entry.name, file_timestamp, file_date))
            # print(f"{entry.name} ({file_date})")
            dir_files.append(f"{entry.name} ({file_date})")
    
    if dir_files:
        colored("Found files:", "green")
        for i in dir_files:
            print(i)

        newest_file = max(files, key=lambda x: x[1])
        print()
        colored(f"The newest file is: {newest_file[0]} ({newest_file[2]})", "green")
        revert = input("Revert permissions to this file? (Y/N): ")

        if revert.lower() in ["y"]:
            print(f"Reverting to {newest_file[0]} \n")
            revert_file_perms(newest_file[0])
        else:
            file = input("Please enter the file name: ")
            revert_file_perms(file)
    else:
        print("Uh oh! Couldn't find any backups... good luck")

                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List file permissions and save them to a file.")
    parser.add_argument('--info', action='store_true', help="Print file permissions and names to the console.")
    parser.add_argument('--revert', action='store_true', help="Reverts file permissions.")
    args = parser.parse_args()
    
    if args.revert:
        find_file_perms()
    else:
        save_file_perms(args.info)
