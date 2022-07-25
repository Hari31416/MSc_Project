# import sys


# def get_slice(pizza):
#     pizza.extend(pizza)
#     mashroom = 0
#     for i in range(len(pizza) - 4):
#         j = i + 4
#         slice = pizza[i:j]
#         assert len(slice) == 4
#         if mashroom < sum(slice):
#             mashroom = sum(slice)
#     return mashroom


# if __name__ == "__main__":
#     pizza = []
#     for i in range(8):
#         pizza.append(int(sys.stdin.readline()))
#     print(get_slice(pizza))

# import sys


# def get_max_avg(array, N, K):
#     max_avg = 0
#     for k in range(K, N):
#         for i in range(len(array) - k + 1):
#             j = i + k
#             slice = array[i:j]
#             print(slice)
#             avg = sum(slice) / k
#             if max_avg < avg:
#                 max_avg = avg
#     return max_avg


# if __name__ == "__main__":
#     N, K = map(int, sys.stdin.readline().split())
#     array = sys.stdin.readline().split()
#     array = list(map(int, array))
#     print(get_max_avg(array, N, K))

import sys


def num_arrows(positions):
    num = 1
    prev = positions[0]
    for pos in positions[1:]:
        new = pos
        if prev - new == 1:
            prev = pos
            continue
        else:
            num += 1
            prev = pos
    return num


if __name__ == "__main__":
    N = int(sys.stdin.readline())
    positions = sys.stdin.readline().split()
    positions = list(map(int, positions))
    print(num_arrows(positions))
