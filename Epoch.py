import subprocess
import os


def train(n = 1, fileName = "BreakoutAI.py"):
    path = os.path.dirname(os.path.realpath(__file__))

    for i in range(n):
       subprocess.run(f"py ./{fileName} &", cwd=path)
       print(f"EPOCH {i}/{n}")


train(n=1000)