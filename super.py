import os
import stat
import time

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

def list_files_stats():
    today = int(time.time())
    current_dir = os.getcwd()
    print("Logging file stats... Please wait. Run with --info to see perms.")
    for entry in os.scandir(current_dir):
        if entry.is_file() or entry.is_dir():
            stats = entry.stat()
            numeric_perm = numeric_permissions(stats.st_mode)
            print(f"{numeric_perm} {entry.name}")

            with open(f"{today}.txt", "a") as f:
                f.write(f"{numeric_perm} {entry.name}")
                f.write('\n')

if __name__ == "__main__":
    list_files_stats()
