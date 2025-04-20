import subprocess
import sys


def main() -> None:
    subprocess.run([sys.executable] + sys.argv[1:])
