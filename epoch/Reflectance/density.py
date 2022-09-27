import sys
import os


def find_and_replace(
    file_name="input.deck",
    find1="DENSITY_FACTOR",
    find2="VECTOR_POTENTIAL",
    replace1=4,
    replace2=0.1,
):
    with open(file_name, "r") as file:
        filedata = file.read()
    filedata = filedata.replace(find1, replace1)
    filedata = filedata.replace(find2, replace2)
    new_dir = f"D_{replace1}_A_{replace2}"
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    new_file_dir = os.path.join(new_dir, file_name)
    new_deck_dir = os.path.join(new_dir, "deck.file")
    with open(new_file_dir, "w") as file:
        file.write(filedata)
    with open(new_deck_dir, "w") as file:
        file.write(".")


if __name__ == "__main__":
    find_and_replace(replace1=sys.argv[1], replace2=sys.argv[2])
