from itertools import combinations


def first_test(iterable, r):
    test = combinations(iterable, r)
    with open('test.txt', 'a') as file:
        [file.write(str(f'{t}\n')) for t in test]


actions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

[first_test(actions, count) for count in range(1, 10)]
