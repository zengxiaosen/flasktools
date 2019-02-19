
class A:
    a = "a"
    b = "b"

    def testA(self):
        print("testA")


class B(A):
    c = "c"
    d = "d"

    def testB(self):
        print("testB")


if __name__ == "__main__":
    oa = A()
    ob = B()
    print(oa.a)
    print(oa.b)
    oa.testA()
    print('---')
    print(ob.a)
    print(ob.b)
    print(ob.c)
    print(ob.d)
    ob.testA()
    ob.testB()
