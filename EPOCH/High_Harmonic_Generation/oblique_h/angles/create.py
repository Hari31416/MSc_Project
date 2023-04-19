import os

ANGLES = ["pi/3", "pi/4", "pi/6", "0", "pi/12"]
DIRS = [3, 4, 6, 0, 12]


def create_one_dir(dir="p"):
    os.makedirs(dir, exist_ok=True)

    with open(f"input_{dir}.deck", "r") as f:
        raw_input = f.read()

    for angle, dir_ in zip(ANGLES, DIRS):
        os.makedirs(f"{dir}/{dir_}", exist_ok=True)
        print(angle)
        input_ = raw_input.replace("ANGLE", angle)

        with open(f"{dir}/{dir_}/input.deck", "w") as f:
            f.write(input_)
        with open(f"{dir}/{dir_}/deck.file", "w") as f:
            f.write(".")


def main():
    directories = ["p", "s"]
    for dir in directories:
        create_one_dir(dir)


if __name__ == "__main__":
    main()
