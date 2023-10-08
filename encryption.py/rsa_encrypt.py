"""
summary:
    Basically, I was interested in learning how encryption worked
    and I started down the rabbit hole. This is for the RSA encryption algo.
    I wanted to walk through an somewhat realistic example and output it.

    The examples I found didn't really mirror real life use cases ( like SSL certs).
    An issue I found was that I've never seen an integer key. So I was wondering why that was.
    My initial guess was that maybe they all got base 64 encoded?

"""



### BUILT-IN LIBS ###
import random
import base64 as b64
import math
import string

### PYPI LIBS ###
from tabulate import tabulate
from Crypto.PublicKey import RSA



######################## FOR USER INPUT ########################
KEY_BIT_SIZE = 256
YOUR_MESSAGE = "This totally fine and optimal."

numbers_to_test = [90, 40, 2, 3, 7, 174440041, 3657500101, 88362852307,
    414507281407, 2428095424619, 4952019383323, 12055296811267,
    17461204521323, 28871271685163, 53982894593057,
    102394248776725249869933727098077036248844242538416910290781872218101184705397]


######################## FUNCTIONS ########################
def calc_num_length_from_bits(bit_size_int):
    """You know when you run stuff from ssh-keygen and you do stuff like:
        ssh-keygen -t rsa -b 4096
    You ever wonder long an integer is if it has 4096 bits?
    Well, this function finds out for you. Here's an explanation

    Number of Digits ≈ (Key Length in Bits) / log₂(10)
    log₂(10) is effectively the size per given integer/decimal "chunk". It comes out to 3.3219

    Args:
        bit_size_int (float): approximate length of the digit

    """

    num_of_digits = bit_size_int/math.log2(10)

    return math.ceil(num_of_digits)

def is_prime(n):
    """Brute Force check if a number is prime

    Args:
        n (int): Number you are testing to be prime

    Returns:
        bool: confirms whether n was a prime or not
    """
    if n <= 1:
        return False
    elif n % 2 == 0:
        return False

    for num in range(2, int(n/2)):
        if n % num == 0:
            print(num)
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

    # Finding the values for k, m to use later
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

    calculated_info = [["bit size", "approximate length"]]
    for to_pwr in range(2, 13):
        bit = 2**to_pwr

        values = [
            bit,
            calc_num_length_from_bits(bit)
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

    prime_size = math.ceil(calc_num_length_from_bits(key_bit_size))


    # Python magic
    start_pad = prime_size*"0"
    end_pad = prime_size*"9"
    start = int(f"1{start_pad}")
    end = int(f"9{end_pad}")
    a_number = random.randint(start, end)

    found_prime = False
    counter =0
    while found_prime is False:
        # Generate some random number based on provided bit size
        # a_number = random.randint(start, end)

        # We want to start with an odd number
        if a_number % 2 == 0:
            a_number = random.randint(start, end)
            continue
        # for _ in range(100):
        a_number +=2
        if is_probably_prime(a_number, 10):
            found_prime = True


        counter+=1

    return a_number

def encode_base64(my_value, encoding_format = "ascii"):
    """Encodes a given value to a base 64 encoded string

    Args:
        my_value (string/int/float): The value you are encoding as a base 64 string
        encoding_format (str, optional): Defaults to "ascii". Determines what encoding will be used.

    Returns:
        string: my_value as a base 64 encoded string
    """
    ascii_bytes = str(my_value).encode(encoding_format)
    encoded_val_as_byte = b64.b64encode(ascii_bytes)
    encoded_val_as_string = encoded_val_as_byte.decode(encoding_format)

    return encoded_val_as_string

def decode_base64(my_value, encoding_format = "ascii"):
    """Decodes a given base 64 string

    Args:
        my_value (string/int/float): The base64 string you are decoding
        encoding_format (str, optional): Defaults to "ascii". Determines what encoding will be used.

    Returns:
        string: my_value as a decoded base64 string
    """
    ascii_bytes = str(my_value).encode(encoding_format)
    return b64.decodebytes(ascii_bytes).decode(encoding_format)

def gcd(a, b):
    """Getting global common denominator using the Euclidian Algorithm.
    I chose a pretty simple implementation since I'm gonna use this for reference.

    large = small * q + remainder
    - large becomes small, r becomes small
    - keep going until remainder == 0 and take previous remainder

    Args:
        a (int): any integer
        b (int): any integer

    Returns:
        int: The largest common global denominator between two numbers.
    """
    # Handing for cases where zero
    if a == 0:
        return b
    elif b == 0:
        return a

    # Setting the larger/smaller numbers
    elif a >= b:
        large, small = a, b
    else:
        large, small = b, a

    remainder = small
    while remainder != 0:
        prev_remainder = remainder
        remainder = large % small
        large = small
        small = remainder

    return prev_remainder

def gcd_extended(a, b):
    """Using Extended Euclidian Algo, it's just the regular one but for finding
        the multiplicative inverse instead. Honestly still don't really
        understand this one.

    Args:
        a (int): a number
        b (int): a number. Must be larger or equal to a.

    Raises:
        ValueError: Raises when a is larger than b

    Returns:
        tuple: tuple of 3 int containing the remainders, and multiplicative inverses.
    """

    if a > b:
        raise ValueError("value a cannot be larger than b")

    # Terminate
    if a == 0:
        return b, 0, 1

    glob_com_denom, x1, y1 = gcd_extended(b % a, a)

    x = y1 - (b//a) * x1
    y = x1
    return glob_com_denom, x, y

def multiplicative_inverse(a, b):
    """Using Extended Euclidian Algo, it's just the regular one but for finding
        the multiplicative inverse instead. Honestly still don't really
        understand this one.

    Args:
        a (int): a number
        b (int): a number. Must be larger or equal to a.
    Raises:
        ValueError: _description_

    Returns:
        tuple: tuple of 3 int containing the remainders, and multiplicative inverses.
    """
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0

def generate_rsa_key_pair(p, q):
    """Generates and rsa key pair

    Args:
        p (int): Prime number
        q (int): Another prime number

    Returns:
        tuple: Returns ((e, n), (d, n), (phi))
    """
    print("> Calculating RSA key pair")
    modulus_rsa = p * q  # Used a the modulus and is public
    print("\tModulus -- p*q:")
    print(f"\t\t{modulus_rsa}")
    phi_rsa = (p-1)*(q-1)
    print("\tphi -- (p-1)*(q-1)")
    print(f"\t\t{modulus_rsa}")

    # Choose encryption num
    # 3 < encrypt_key < phi_rsa
    # Coprime with n and oN - no number chosen can be factor of either number
    #   As such,  the GCD of encrypt_key and phi_rsa must be equal to 1
    print("\tChoosing a random encrypt_key between 1 < encrypt_key < phi_rsa")
    print("\tNOTE: No number chosen can be factor of either number")
    common_denominator = None
    encrypt_key = None
    e_attempts = 0
    while common_denominator != 1:
        encrypt_key = random.randrange(3, phi_rsa)
        e_attempts +=1
        print(f"\t\t Selecting a random number...Attempt {e_attempts}")
        # The number chosen must always be odd
        if encrypt_key % 2 == 0:
            continue
        #     encrypt_key = encrypt_key - 1
        common_denominator = gcd(encrypt_key, phi_rsa)

    print(f"\tPublic Encryption Key Selected:\n\t\t{encrypt_key}")
    # Determine decryption key
    # encrypt_key * decrypt_key mod (phi) = 1

    print("\tDetermining the decryption key -- encrypt_key * decrypt_key mod (phi) = 1")
    mi = multiplicative_inverse(encrypt_key, phi_rsa)[1]
    if mi > 0:
        decrypt_key = mi
    else:
        decrypt_key = mi + phi_rsa
    print(f"\tPrivate Decryption Key Selected:\n\t\t{decrypt_key}")
    kp = ((encrypt_key, modulus_rsa), (decrypt_key, modulus_rsa), (phi_rsa))
    return kp

def create_char_to_num_map():
    """When you encrypt a given character, you need be able to assign it some common ground
    numerical value. I'm not sure what the standard is especially when you start considering
    encodings and special characters.

    Returns:
        dict: dict mapping every printable character to a numerical value
    """
    values = {}
    for index, character in enumerate(string.printable):
        values[character] = index
    return values

def create_num_to_char_map():
    """Used to create a map mapping numbers to every printable character.

    Returns:
        dict: dict mapping numerical value to every printable character
    """
    values = {}
    for index, character in enumerate(string.printable):
        values[index] = character
    return values

def text_to_integers(your_text, text_num_map = None):
    """_summary_

    Args:
        your_text (_type_): _description_
        text_num_map (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    if text_num_map is None:
        text_num_map = create_char_to_num_map()

    return [ text_num_map[char_x] for char_x in your_text]

def encrypt_integers(encryption_keypair, my_integers):
    """_summary_

    Args:
        encryption_keypair (_type_): _description_
        my_integers (_type_): _description_

    Returns:
        _type_: _description_
    """

    my_e, my_m = encryption_keypair
    return [pow(num_i, my_e, my_m) for num_i in my_integers]

def decrypt_integers(decryption_keypair, my_encrypted_integers):
    """_summary_

    Args:
        decryption_keypair (_type_): _description_
        my_encrypted_integers (_type_): _description_

    Returns:
        _type_: _description_
    """
    my_decryption_key, my_modulus = decryption_keypair
    return [pow(encrypted_num, my_decryption_key, my_modulus)
                for encrypted_num in my_encrypted_integers]


def integers_to_text(your_integers, num_text_map = None):
    """_summary_

    Args:
        your_integers (_type_): _description_
        num_text_map (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """

    if num_text_map is None:
        num_text_map = create_num_to_char_map()

    separated_characters = [ num_text_map[int_x] for int_x in your_integers]

    return "".join(separated_characters)
# encrypted = pow(INT_VAL, e, em)
# decrypted = pow(encrypted, d, dm)

################################ BODY ################################
print_bit_to_int_length_explanation()

print(f"\n************** Generating {KEY_BIT_SIZE} bit RSA keys **************")
print(f"> RSA encryption bit size: {KEY_BIT_SIZE}")

if not is_valid_bit_size(KEY_BIT_SIZE):
    raise ValueError("Not valid bit size")

HALF_BIT = int(KEY_BIT_SIZE/2)
digit_length = round(calc_num_length_from_bits(KEY_BIT_SIZE), 2)
print(f"> Your private & public key will be {KEY_BIT_SIZE} bits (~{digit_length} digits)\n")


prime_one = generate_prime_number(HALF_BIT)
prime_two = generate_prime_number(HALF_BIT)

print(f"> Random Prime Number 1 (p):\n\t{prime_one}\n---")
print(f"> Random Prime Number 2 (q):\n\t{prime_two}\n")

my_keys = generate_rsa_key_pair(prime_one, prime_two)
demo_modulus = my_keys[0][1]
demo_ek = my_keys[0][0]
demo_dk = my_keys[1][0]
phi = my_keys[2]

# print(my_keys)
# print("-" * 8, f"\n> Modulus:\n\t{demo_modulus}\n\tLength: {len(str(demo_modulus))}")
# print("-" * 8, f"\n> Public Encryption Key:\n\t{demo_ek}\n\tLength: {len(str(demo_ek))}")
# print("-" * 8, f"\n> Private Decryption Key:\n\t{demo_dk}\n\tLength: {len(str(demo_dk))}")


check_encrypt = gcd(demo_ek, demo_modulus)
check_decrypt = (demo_ek * demo_dk) % phi
print("\n> Checking Encryption key")
print(f"\tGCD(encryption_key, modulus) = {check_encrypt}")
print("> Checking Decryption key")
print(f"\t(encryption_key * decryption_key) % phi = {check_decrypt}\n")

if check_encrypt != 1:
    raise ValueError("Bad encrypt key: GCD of encryption key and modulus is != 1")
elif check_encrypt != 1:
    raise ValueError("Bad decrypt key: (encryption_key * decryption_key) % phi != 1")

char_to_num_map = create_char_to_num_map()
num_to_char_map = create_num_to_char_map()



mytext_to_integers = text_to_integers(YOUR_MESSAGE)
joined_text = ','.join(str(x77) for x77 in mytext_to_integers)

print("> Converting your message to numbers text based on ASCII encoding")
print(f"\tYour message: '{YOUR_MESSAGE}' Became:")
print(f"\t{joined_text}\n")

encrypted_integers = encrypt_integers((demo_ek, demo_modulus), mytext_to_integers)

print("> Converting your numerical message to cipher numbers")
print("\tUsing your Encryption key, your cipher numbers became:")
joined_enc_numbers = ','.join(str(x9) for x9 in encrypted_integers)
if len(joined_enc_numbers) > 500:
    joined_enc_numbers = f"{joined_enc_numbers[1:120]}....(REALLY long number)"
print(f"\t{joined_enc_numbers}\n")

decrypted_integers = decrypt_integers((demo_dk, demo_modulus),encrypted_integers)
print("> Decrypting your encrypted cipher numbers")
print("\tUsing your Decryption key, your cipher numbers became:")
print(f"\t{','.join(str(x16) for x16 in decrypted_integers)}\n")

decrypted_message = integers_to_text(decrypted_integers)
print("> Converting the decrypted cipher numbers back to your original message:")
print("\tUsing a mapping of integer to ASCII characters:")
print(f"\t\t{decrypted_message}\n")

formal_rsa = RSA.construct((demo_modulus, demo_ek, demo_dk), consistency_check=True)
pem_private = formal_rsa.export_key().decode("ascii")
pem_public = formal_rsa.publickey().export_key().decode("ascii")
print("> Your Public Key in PEM format:")
print(f"{pem_public}\n")

print("> Your Private Key in PEM format:")
print(f"{pem_private}")














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
