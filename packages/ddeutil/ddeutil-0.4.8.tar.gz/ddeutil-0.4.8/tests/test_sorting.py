from ddeutil.core import sorting


def test_ordered():
    assert sorting.ordered([[11], [2], [4, 1]]) == [[1, 4], [2], [11]]
    assert sorting.ordered({1: [8, 12, 5]}) == {1: [5, 8, 12]}


def test_sort_priority():
    assert sorting.sort_priority(values=[1, 2, 2, 3], priority=[2, 3, 1]) == [
        2,
        2,
        3,
        1,
    ]
    assert sorting.sort_priority(values={1, 2, 3}, priority=[2, 3]) == [2, 3, 1]
    assert sorting.sort_priority(values=(1, 2, 3), priority=[2, 3]) == [2, 3, 1]
    assert sorting.sort_priority(
        values=(1, 2, 3), priority=[2, 3], mode="enumerate"
    ) == [2, 3, 1]

    assert sorting.sort_priority(
        values=[1, 2, 1], priority=[2, 3], mode="foo"
    ) == [1, 2, 1]
