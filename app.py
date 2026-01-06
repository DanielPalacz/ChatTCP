import subprocess
import sys
import multiprocessing

def run_via_multiprocess():
    subprocess.run([sys.executable, "client.py"])


for _ in range(2):
    process = multiprocessing.Process(target=run_via_multiprocess, args=())
    process.start()
