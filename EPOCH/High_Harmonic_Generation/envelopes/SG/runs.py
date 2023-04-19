import os
import sys


def prepare_one(p, ratio):
    path_dir = f"./SG_{p}"
    if not os.path.exists(path_dir):
        os.mkdir(path_dir)
    with open("input.deck", "r") as f:
        data = f.read()
    data = data.replace("p_value", str(p))
    data = data.replace("area_ratio_value", str(ratio))
    with open(f"./SG_{p}/input.deck", "w") as f:
        f.write(data)

    with open(f"SG_{p}/deck.file", "w") as f:
        f.write(".")


def prepare(p_list, ratio_list):
    for p, ratio in zip(p_list, ratio_list):
        prepare_one(p, ratio)


def main():
    # ratios = {
    #     2: 1.0,
    #     4: 1.1617448070082612,
    #     6: 1.2025442073509194,
    #     8: 1.2193552309287747,
    #     10: 1.2280600036588267,
    #     12: 1.2332802909912786,
    # }
    ratios = {
        # 2: 1.0,
        # 4: 1.1617448070082612,
        # 6: 1.2025442073509194,
        # 8: 1.2193552309287747,
        # 10: 1.2280600036588267,
        # 12: 1.2332802909912786,
        14: 1.237062945132788,
        16: 1.24019733213889,
        18: 1.2424605543438842,
        # 20: 1.2442253903686272,
    }

    p_list = list(ratios.keys())
    ratio_list = list(ratios.values())
    prepare(p_list, ratio_list)
    cmd = "epoch1d < deck.file"
    for p in p_list:
        print(f"Running SG_{p} ...")
        os.system(f"cd SG_{p}; {cmd}; cd ..")


if __name__ == "__main__":
    main()
