import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.facebookApi import get  # noqa: E402


def test_get_data1():
    response = get("email,name")
    assert type(response) is list


def test_get_data2():
    response = get("gender,birthday")
    assert type(response) is list


if __name__ == "__main__":
    test_get_data1()
    test_get_data2()
    print("All tests passed.")
