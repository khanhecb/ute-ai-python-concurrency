import multiprocessing
import sys
from path import Path

def search(keyword, paths, output):
    lines = []
    for path in paths:
        lines.extend(l.strip() for l in path.open())

    for line in lines:
        if keyword in line:
            output.put(line)

def divide_paths(paths, n):
    avg = len(paths) // n
    out = []
    for i in range(n):
        out.append(paths[i*avg:(i+1)*avg])
    return out

if __name__ == "__main__":
    keyword = sys.argv[1]
    folder = sys.argv[2]
    folder = Path(folder)

    paths = list(folder.walkfiles())
    nprocs = 4
    output = multiprocessing.Queue()

    chunks = divide_paths(paths, nprocs)
    procs = []

    for chunk in chunks:
        p = multiprocessing.Process(target=search, args=(keyword, chunk, output))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

    results = []
    while not output.empty():
        results.append(output.get())

    for line in results:
        print(line)
