def exampleFunction(x, y):
    if x < 0:
        print("Negative")
    else:
        print("Positive")
        if x == 0:
            print("Zero")
    return x * 2


class myclass:
    def myMethod(self):
        print("Hello, World!")


if __name__ == "__main__":
    exampleFunction(5, 10)
    exampleFunction(-1, 10)
    exampleFunction(0, 0)
