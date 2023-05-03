import os
import sys


def prepare_one(run, length):
    path_dir = f"./{run}"
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    with open("input.deck", "r") as f:
        data = f.read()
    data = data.replace("RAMP_LENGTH", str(length))
    with open(f"./{run}/input.deck", "w") as f:
        f.write(data)


def main():
    lengths = range(12, 21, 2)
    for length in lengths:
        prepare_one(f"run_{length}", round(length * 0.1, 1))


if __name__ == "__main__":
    main()
