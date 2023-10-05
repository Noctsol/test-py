"""

"""

import random
import math

def miller_rabin(n, k):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def is_probably_prime(n, attempts):
    """ This function determines wether a number is a prime or not.
    It uses the Miller-Rabin primality test. For a much longer explanation,
    Read the "MILLERRABINSTUFF" (use ctrl+f) section below.
    """

    if n < 2:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0:
        return False

    # # Finding the values for k, m to use later
    k = 0
    m = n - 1
    while m % 2 == 0:
        k += 1
        m //= 2

    # Running through randomized tests to check
    for _ in range(attempts):
        a = random.randint(2, n-1)
        m = int(m)
        b = pow(a, m, n)   # a**m%n

        if b == 1 or b == n-1:
            continue
        else:
            is_prime = False
            for _ in range(k-1):
                b = pow(b, 2, n)
                if b == n - 1 :
                    is_prime = True
                    break

            if not is_prime:
                return False
    return True




# primes = [90,40, 2,3,7,174440041, 3657500101, 88362852307,
#           414507281407, 2428095424619, 4952019383323, 12055296811267,
#           17461204521323, 28871271685163, 53982894593057]

# for i in primes:
#     # print(i, is_prime_millerrabin1(i, 40))
#     print(i, is_probably_prime(i, 40))



# for i in range(30,50):
#     d = i
#     stuff = []
#     for k in range(1,5):
#         a = (d-1)/(2**k)
#         stuff.append((f"a{k}", a))
#     print(i, stuff)
long = 102394248776725249869933727098077036248844242538416910290781872218101184705397
long2 = 102394248776725249869933727098077036248844242538416910290781872218101184705397
answer = 25598562194181312467483431774519259062211060634604227572695468054525296176349
# import math

# long = 16-1
# long2 = 16-1
# answer = 25598562194181312467483431774519259062211060634604227572695468054525296176349

# for i in range(0,4):
#     print(i, math.floor((long)/(2**i+1)), "--")
#     long2//=2
#     print(i, long2, "--")

# print(long)
print(is_probably_prime(long,100))
print(miller_rabin(long,100))

print(2**2)

# n = 49

# r, s = 0, n - 1
# while s % 2 == 0:
#     r += 1
#     s = s // 2

# print(n)

# 16/2 = 8
# 8/2 = 4
# 4/2 =2

# 16

print(51197124388362624934966863549038518124422121269208455145390936109050592352698*2)

# 2 51197124388362625725133409835076597863915334738526892293414951707394900492288
# 2 25598562194181312467483431774519259062211060634604227572695468054525296176349