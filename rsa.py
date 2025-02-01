import math
import random

'''
The following program performs RSA encryption on a plaintext message, and then decrypts the message.
We simulate the encryption, decryption, and transmission of the message through print statements. 

# Standard Key Size 1024->4096 Bits long
# Primes Generated 1024->2048 Bits
# Modulus Size from 2048->4096 Bits
# Must be divisible by 256

RSA Encryption formula: C = M^e mod n, where 
    C is the ciphertext
    M is the plaintext
    e is the public exponent
    n is the modulus

RSA Decryption formula: M = C^d mod n

Key generation for RSA: 
    > Choose two large prime numbers, p and q
    > Compute n = p x q. N represents the modulus in the public/private keys.
    > Compute euler's totient: phi ( ϕ(n)=(p-1)(q-1) ).
    > Choose an e that is coprime with Euler's totient, i.e gcd(e, ϕ(n)) == 1
    > d = the modular inverse of e mod phi
    > Generate public key as tuple (e, d) and private key as tuple (d, n)

'''
# Definition: Wrap the program in a function to call from projectGUI 
# Parameters: N/A
# Returns: N/A
def runRSA():
    # Definition: Encrypts message using RSA algorithms
    # Parameters: message (as an array of ASCII values (integers), publicKey, and integer n (modulus in RSA) 
    # Returns: list of encrypted integers (the ciphertext)
    def encrypt(message, publicKey):
        cipherText = []
        e, n = publicKey # unpack the public key

        # Iterate through each letter in the message
        for ascii_val in message:
            # Cannot be 0
            encryptText = 1

            # Perform modular exponentiation (M ^ e % n)
            # Loop e times to compute M ^ e
            # Logic: C = M^e mod n
            #   Iteration 1: encryptText (C) = 1 X ASCII mod n (M^1 mod n)
            #   Iteration 2: encryptText (C) = encryptText x ASCII mod n (M^2 mod n)
            #   Iteration e: encryptText (C) = encryptText x ASCII mod n (M^e mod n)
            for _ in range(e):
                encryptText *= ascii_val
                # ensure result is within bounds of n
                encryptText %= n 
        
            # Append the encrypted value to the final list 
            cipherText.append(encryptText)

        return cipherText
    
    # Definition: Decrypts an array of encrypted values and returns an array of ASCII Characters
    # Parameters: message(list): the encrypted message as an array of integers (ciphertext), privatekey, integer n 
    # Returns: the decrypted message as a string
    def decrypt(message, privateKey):
        final = []
        d, n = privateKey # unpack private key

        # Oterate through encrypted values
        for encrypted_val in message:
            decryptText = 1   # Cannot be 0

            # Perform modular exponentiation (encrypted_val % n) for decryption 
            # Loop d times to compute M ^ d
            # Logic: RSA Decryption formula: M = C^d mod n
            #   Iteration 1: decryptText (M) = 1 X ASCII mod d (C^1 mod n)
            #   Iteration 2: decryptText (M) = decryptText x ASCII mod n (C^2 mod n)
            #   Iteration d: decryptText (M) = decryptText x ASCII mod n (C^d mod n)
            for _ in range(d):
                decryptText *= encrypted_val
                decryptText %= n # Keep the result within bounds of n
            final.append(decryptText)
        
        # Convert the decrypted integer back to the character
        plaintext = ASCII2string(final)
        return plaintext
    
    # Definition: Appends all prime numbers between 2 and upper limit to list of prime numbers (prime_num).
    # Parameters: int upper
    # Returns: List of prime numbers up to "upper"
    def gen_prime(upper):
        prime_nums = []
        for num in range(2, upper + 1):
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                prime_nums.append(num)
        return prime_nums

    # Definition: Picks a random prime number from a list
    # Parameters: List of prime numbers
    # Returns: A random prime number
    def get_prime(prime_num):
        # Generating Random Iterator to select from Prime Array
        length = len(prime_num)
        a = random.randint(0, length - 1)

        # Choose a random prime 
        prime = prime_num[a]

        # Deletes the Prime number that is chosen so subsequent call ensures it is not chosen again
        prime_num.remove(prime)
        return prime

    # String to ASCII conversion
    def string2ASCII(text):
        ASCII = list(text.encode('ascii'))
        return ASCII

    # ASCII to String Convertion
    def ASCII2string(encoded):
        string = ""
        for num in encoded:
            string += (chr(num))
        return string
  
    # Text to Encrypt
    Text = "Hello, Welcome to RSA Encryption!"
    print("Message to encrypt: ", Text, '\n')

    print("Cipher Text = Message ^ e mod n")
    print("Plaintext = CipherText ^ d mod n", '\n')

    # Establish an Upper Range to choose a Random Prime. 
    upper = 1000

    # Generate a list of prime numbers within bounds of upper
    prime_num = gen_prime(upper)
    
    print("Selecting Two Random Primes Numbers: ")

    # Assigns P and Q to be 2 Random Primes
    p = get_prime(prime_num) 
    q = get_prime(prime_num)
    print("Prime 1 (p): ", p)
    print("Prime 2 (q): ", q, '\n')

    # calculate n (modulus)
    n = p * q

    # calculate Euler's totient ϕ(n)
    phi = (p - 1) * (q - 1)
    
    print("Calculate n = (p * q): ", n)
    print("Calculate Euler's totient of n = ϕ(n): ", phi, '\n')
    
    # Intialize e and find a suitable e where gcd(e, ϕ(n)) == 1
    # e must be coprime with ϕ(n), so start with small value and loop until found 
    # e is the public exponent in the public key (M ^ e mod n)
    # start searching from 2 as 0 and 1 would not satisfy the conditions:

    e = 2 # does not need to be random 
    while math.gcd(e, phi) != 1:
        e += 1
    
    # Final Value of e will part of the Public Key
    publicKey = (e, n) # Public key is the pair (e, n)

    print("PublicKey = (e, n) where 1 < e < ϕ(n) and GCD(e, ϕ(n)) == 1")
    print("Public Key:", publicKey, '\n')

    # Initialize d and find a suitable d where (d * e) % φ(n) == 1
    # This ensures that d is the modular inverse of e module φ(n)
    # d is the private exponent in the private key (C ^ d mod n)
    # start searching from 2 as 0 and 1 would not satisfy the conditions
    d = 2
    while (d * e) % phi != 1:
        d += 1

    # Final Value of d will be the Public Key
    privateKey = (d, n) 

    print("Private Key = (d, n) where (d * e) % ϕ(n) == 1")
    print("Private Key:", privateKey, '\n')

    # Convert plaintext to equivalent list of ASCII integers in order to perform modular exponentiation
    asciiText = string2ASCII(Text)
    print(f"Pre-encryption - Plaintext represented as a list of ASCII characters: {asciiText}\n")

    # Perform the encryption on sender's side 
    cipherText = encrypt(asciiText, publicKey)
    print(f"Post-encryption - Ciphertext represented as a list of encrypted ASCII characters: {cipherText} \n")

    print("Transmitting cipher to receiver...\n")
    print("Receiver uses their private key to decrypt the ciphertext...\n")
    # Perform the decryption on the receiver's side 
    plaintext = decrypt(cipherText, privateKey)

    print(f"Final Decrypted Text: {plaintext}")

runRSA()
