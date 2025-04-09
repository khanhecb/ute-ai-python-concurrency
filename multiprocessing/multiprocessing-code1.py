from multiprocessing import Process, cpu_count
import time
import os

class MuchCPU(Process):
    def run(self):
        print(os.getpid())  # Sửa getped() thành getpid()
        for i in range(200_000_000):
            pass

if __name__ == '__main__':
    procs = [MuchCPU() for _ in range(cpu_count())]  # đổi f thành _
    t = time.time()
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print('work took {} seconds'.format(time.time() - t))