from itertools import combinations


def first_test(iterable, r):
    test = combinations(iterable, r)
    [print(t) for t in test]


actions = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

[first_test(actions, count) for count in range(1, 10)]
