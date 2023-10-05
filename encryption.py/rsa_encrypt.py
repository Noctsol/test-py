"""
author: noctsol
created_date: 2023-01-22
summary:
    Basically, I was interested in learning how encryption worked
    and I started down the rabbithole. This is for the RSA encryption algo.
    I wanted to walk through an somewhat realistic example and output it.

    The examples I found didn't really mirror real life use cases ( like SSL certs).
    An issue I found was that I've snever seen an integer key. So I was wondering why that was.
    My initial guess was that maybe they all goit base 64 encoded?

"""



### BUILT-IN LIBS ###
import random
import base64
import math

### PYPI LIBS ###
from tabulate import tabulate

######################## FOR USER INPUT ########################
KEY_BIT_SIZE = 1024

numbers_to_test = [90, 40, 2, 3, 7, 174440041, 3657500101, 88362852307,
    414507281407, 2428095424619, 4952019383323, 12055296811267,
    17461204521323, 28871271685163, 53982894593057,
    102394248776725249869933727098077036248844242538416910290781872218101184705397]



def calc_num_length_from_bits(bit_size_int, approximate=True):
    """You know when you run stuff from ssh-keygen and you do stuff like:
        ssh-keygen -t rsa -b 4096
    You ever wonder long an integer is if it has 4096 bits?
    Well, this function finds out for you. Here's an explanation

    Number of Digits ≈ (Key Length in Bits) / log₂(10)
    log₂(10) is effectively the size per given integer/decimal "chunk". It comes out to 3.3219

    since 3.3219 bits exists is NOT a thing. You can round up to 4. So the equation becomes.
        Number of Digits ≈ (Key Length in Bits) / 4
    Args:
        bit_size_int (_type_): _description_

    """
    if approximate is True:
        numofdigits = int(bit_size_int/4)
    else:
        numofdigits = bit_size_int/math.log2(10)
    return numofdigits


def is_prime(n):
    """_summary_

    Args:
        n (int): Number you are testing to be prime

    Returns:
        bool: confirms whether n was a prime or not
    """
    if n <= 1:
        return False
    elif n % 2 == 0:
        return False

    for i in range(2, int(n/2)):
        if n % i == 0:
            print(i)
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
            is_prime_temp = False
            for _ in range(k-1):
                b = pow(b, 2, n)
                if b == n - 1 :
                    is_prime_temp = True
                    break

            if not is_prime_temp:
                return False
    return True



def print_bit_to_int_length_explanation():
    """Generates a table for you that will explain the rough length of
    of a digit given you requested key bit size from 2-4096 bits.
    """

    calculated_info = [["bit size", "approximate length", "exact length"]]
    for i in range(1, 13):
        bit = 2**i

        values = [
            bit,
            calc_num_length_from_bits(bit),
            calc_num_length_from_bits(bit, False)
        ]
        calculated_info.append(values)

    print(tabulate(calculated_info))


def is_valid_bit_size(bit_size):
    """Checks if the bit size requested is valise from the base 2 system.

    Args:
        bit_size (int): some chosen bit size

    Returns:
        bool: Indicates whether this is a valid bit size or not
    """

    if bit_size == 0:
        return False

    raised_power = math.log2(bit_size)
    if not raised_power.is_integer():
        return False

    return True


def generate_prime_number(key_bit_size):
    """_summary_

    Args:
        bit_size (_type_): _description_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """

    if not is_valid_bit_size(key_bit_size):
        raise ValueError(
            f"{key_bit_size} is not valid. Please enter in a valid bit size")

    prime_size = calc_num_length_from_bits(key_bit_size)-1


    # Python magic
    start_pad = prime_size*"0"
    end_pad = prime_size*"9"
    start = int(f"1{start_pad}")
    end = int(f"9{end_pad}")
    a_number = random.randint(start, end)
    # myrange = range(start, end)

    found_prime = False
    counter =0
    while found_prime is False:
        # Generate some random number based on provided bit size
        # a_number = random.randint(start, end)
        # a_number = random.choice(myrange)

        # We want to start with an odd number
        if a_number % 2 == 0:
            a_number = random.randint(start, end)
            continue
        # for _ in range(100):
        a_number +=2
        if is_probably_prime(a_number, 5):
            print("--"*40)
            found_prime = True


        counter+=1

    return a_number


print_bit_to_int_length_explanation()

if not is_valid_bit_size(KEY_BIT_SIZE):
    raise ValueError("Not valid bit size")

split_size = int(KEY_BIT_SIZE/2)

private_num = generate_prime_number(split_size)
public_num = generate_prime_number(split_size)

print(private_num)
print(public_num)


print(f"------------ Generating {KEY_BIT_SIZE} RSA keys ------------")
print("---> Testing Prime Numbers")

for i in numbers_to_test:
    print(f"is {i} a prime number? {is_probably_prime(i, 5)}")


# NOTE: currently trying to figure out how encoding with keys work
# Convert the integer into bytes (binary representation)
rsa_key_bytes = private_num.to_bytes((private_num.bit_length() + 7) // 8, byteorder='big')
rsa_pubkey_bytes = public_num.to_bytes((public_num.bit_length() + 7) // 8, byteorder='big')
# Base64-encode the binary data
base64_encoded_key = base64.b64encode(rsa_key_bytes).decode('utf-8')
base64_encoded_pubkey = base64.b64encode(rsa_pubkey_bytes).decode('utf-8')
print(base64_encoded_key)
print(base64_encoded_pubkey)
# print(base64.b64decode(base64_encoded_key).decode('base64'))
# print(base64.b64decode(base64_encoded_pubkey).decode('base64'))

decoded = int.from_bytes(base64_encoded_key, "big")
print(decoded)












# """
# MILLERRABINSTUFF
#     Normally, when you're writing code for
#     practice questions, you tend to brute force check if a number is prime or not
#     like the is_prime() function here.

#     The brute force method pretty much no longer works when doing encryption as it
#     deals with large numbers (200+ digits). Brute force checking  all digits from
#     2 to 10^n can get pretty bad pretty quick. You need to apply something like
#     a probabilistic check to quickly check your number. The Miller-Rabin primality test
#     is the one currently used by openssl(I think).

#     Don't ask me why this method works. I know enough math for most things,
#     but not this one. I only know how to do it.

#     https://www.youtube.com/watch?v=qdylJqXCDGs

#     --- STEP 1: SOLVE FOR k,m BY USING n-1=(2^k)*m ---

#     You essentially need to test the value of at least once until m is a whole number.
#     Though the proper method is to go all the way down until you find a number that
#     isn't whole and take the previous result.

#     We are going so assume we are checking the number 53
#     To get k,m, you go through the following based on (53-1)/2^k = m:
#     - Attempt 1: (53-1)/2^1 = 26       # Most examples you see will use this one
#     - Attempt 2: (53-1)/2^2 = 13       # You take this value
#     - Attempt 3: (53-1)/2^3 = 6.5      # IGNORED - not a whole number

#     k = 2
#     m = 13

#     --- STEP 2: CHOOSE A RANDOM value ---
#     Test value 1 < a < n -1

#     Args:
#         n (int): Number you are checking if prime
#         attempts (int): amount of times we are going to test n

#     --- STEP 3: TEST a^m mod n ---
#     Using n= 53, k = 2, m = 13 at the example to plug into a^m mod n

#         OUTCOME DECISION TREE 1
#         - Result is 1, means the number is prime probably.
#         - Result is n-1, means the number is prime probably.
#         - Result is not any above, the number is NOT prime. Further calculations needed.

#         ACTUAL OUTCOME 1 (n= 53, k = 2, m = 13  a^m mod n)
#         2^12 mod(53) = 30  # 30 will be represented by b0

#         In this case, since it was 30(b0) we have to another calculation that
#         we will repeat k times. We will use b0^2 mod n. We will iterate through this
#         k times with b0 becoming the previous calculated value until we get to our
#         desired outcome which will be:

#         OUTCOME DECISION TREE 2
#         - Result is 1, the number is NOT prime and is a composite number
#         - Result is n-1, the number is probably prime
#         - Result is not any above, the number is NOT prime

#         ACTUAL OUTCOME 2 (b0^2 mod)
#         30^2mod(53) = 52

#         In this case, we get 52 which is equal to n-1. The number is prime probably.

#         PRETEND OUTCOME
#         Lets say we checking 54 instead at this portion. These is what happens:
#         30^2mod(54) = 36
#         36^2mod(54) = 0      # Note how I use 36 from the previous answer
#         --- No need to go further at this point as we have check k (2) times

#         Thus, finally, we can say that 53 is prime. PROBABLY.
# """
