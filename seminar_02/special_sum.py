
def calculate_special_sum(n):
    """Calculates :math:`\Sum_1^{n-1} (i * (i+1))`.
    
    Parameters
    ----------
    n : int
        Natrual number

    Returns
    -------
    z : int
        The result.
    """
    return sum((i + 1) * i for i in range(1, n))


if __name__ == "__main__":
    f = calculate_special_sum
    f(3) == 8
