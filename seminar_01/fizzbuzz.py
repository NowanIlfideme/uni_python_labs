
if __name__ == "__main__":
    def f(k):
        if k % 3:
            if k % 7:
                return str(k)
            return "Buzz"
        if k % 7:
            return "Fizz"
        return "FizzBuzz"

    lo, hi = 1, 101
    print(" ".join(f(i) for i in range(lo, hi + 1, 2)))
