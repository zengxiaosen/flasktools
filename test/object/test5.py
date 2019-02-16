import json


class test5:
    a = str()
    b = str()


def changeValue(test):
    test.a = 3


if __name__ == "__main__":
    test = test5()
    test.a = 1
    test.b = 2
    # changeValue(test)
    # error
    # test["a"] = '1'
    # test["b"] = '2'
    # print(json.dumps(test, default=lambda o: o.__dict__))
    dic = dict(
        a = "a",
        b = "b"
    )
    dic = dict(test)
    print(dict)
