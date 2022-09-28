import sys
import os


def find_and_replace(
    dir = ".",
    file_name="input.deck",
    find1="0.1 * femto",
    replace1="0.05 * femto",
):
    file_name = os.path.join(dir, file_name)
    with open(file_name, "r") as file:
        filedata = file.read()
    filedata = filedata.replace(find1, replace1)
    # filedata = filedata.replace(find2, replace2)
    # new_dir = f"D_{replace1}_A_{replace2}"
    # if not os.path.exists(new_dir):
    #     os.makedirs(new_dir)
    # new_file_dir = os.path.join(new_dir, file_name)
    # new_deck_dir = os.path.join(new_dir, "deck.file")
    with open(file_name, "w") as file:
        file.write(filedata)

if __name__ == "__main__":
    find_and_replace(dir = sys.argv[1])
