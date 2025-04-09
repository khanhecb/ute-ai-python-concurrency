#!/usr/bin/env python3.10
# Description: Find all file .py in Folder
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from collections import deque

PATH_DIR = '/home/ecb/MEGA' 

def find_files(path: Path, query_string: str):
    subdirs = []
    for p in path.iterdir():
        full_path = str(p.absolute())
        if p.is_dir() and not p.is_symlink():
            subdirs.append(p)
        if query_string in full_path:
            print(full_path)
    return subdirs

def main():
    query = '.py' 
    futures = deque()
    basedir = Path(PATH_DIR) 

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures.append(executor.submit(find_files, basedir, query))

        while futures:
            future = futures.popleft()

            if future.done():
                if future.exception():
                    print(f"Error: {future.exception()}")
                    continue

                subdirs = future.result()
                for subdir in subdirs:
                    futures.append(executor.submit(find_files, subdir, query))
            else:
                futures.append(future)

if __name__ == "__main__":
    main()
