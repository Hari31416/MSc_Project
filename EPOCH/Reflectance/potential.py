import sys
import os


def find_and_replace(file_name="input.deck", find="VECTOR_POTENTIAL", replace=0.1):
    with open(file_name, "r") as file:
        filedata = file.read()
    filedata = filedata.replace(find, replace)
    new_dir = f"A0_{replace}"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file_dir = os.path.join(new_dir, file_name)
    with open(new_file_dir, "w") as file:
        file.write(filedata)


if __name__ == "__main__":
    find_and_replace(replace=sys.argv[1])
