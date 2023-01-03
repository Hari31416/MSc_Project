import os

def main():
    runs = list(range(1, 15))
    densities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25]
    assert len(runs) == len(densities), "runs and densities must be the same length"
    for run, density in zip(runs, densities):
        dir = f"run_{run}"
        if not os.path.exists(dir):
            os.makedirs(dir)
        file_name = os.path.join(dir, "input.deck")
        input_file = "input.deck"
        deck_file = os.path.join(dir, "deck.file")
        with open(input_file, "r") as file:
            text = file.read()
        text = text.replace("FACTOR", str(density))

        with open(file_name, "w") as file:
            file.write(text)
        
        with open(deck_file, "w") as file:
            file.write(".")

if __name__ == "__main__":
    main()
