 

def exchange_money_z(x, coins=(1, 2, 5, 10)):
    """Number of ways to return change of size x, given my params.
    
    Parameters
    ----------
    x : int
        Number between 0 and self.maxnum (default 50).

    Returns
    -------
    res : int
        Different number of ways to get change from self.coins.
    """
    
    if not x or not coins:  # if x == 0 or len(coins) == 0
        return 0

    v = x
    c = coins[0]
    res = 0
    while v > 0:
        res += exchange_money_z(v, coins=coins[1:])
        v -= c
    if v == 0:
        res += 1
    return res


f = exchange_money_z


def exchange_money(x, coins=(1, 2, 5, 10)):
    """Number of ways to return change of size x, given my params.
    
    Parameters
    ----------
    x : int
        Number between 0 and self.maxnum (default 50).

    Returns
    -------
    res : int
        Different number of ways to get change from self.coins.
    """    
    if x == 0:
        return 1
    return exchange_money_z(x, coins=coins)


g = exchange_money
