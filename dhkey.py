import random

'''
The following program implements the Diffie-Hellman key exchange algorithm to allow two parties to securely exchange cryptographic keys over an insecure channel.
We simulate the process of key exchange through print statements, showing how both parties independently generate the same shared secret key.
This program was developed to demonstrate the Diffie-Hellman protocol, which enables secure communication by exchanging public values and deriving a shared private key.

Diffie-Hellman is based on the difficulty of solving the discrete logarithm problem. 
The core of the algorithm involves each party selecting a private key and computing a public value, then exchanging their public values. 
Once both parties have exchanged their public values, they use their own private key and the received public value to compute a shared secret key.

Key Generation:
    Private Key (Xa and Xb): Randomly chosen by each party and kept secret.
    Public Key (Ya and Yb): Computed from the private key using a generator g and a prime number q

Key Exchange:
    Shared secret: Both parties independently compute the shared secret by raising the other party's public key to their own private key modulo q.
'''

def runDH():
    # Definition: Generate and assign private keys for both participant
    # Parameters: N/A
    # Returns: updates the global variables for the private keys of each participant
    def assign_private_key():
        global private_key_k1, private_key_k2, G
        print("Generate Private Keys for Users.\nChoosing random integer between 1000 and 10000 (Much larger range used for production implementations).\n")
        
        private_key_k1 = random.randint(1000, 10000)
        print("Alex Private Key (Xa): ", private_key_k1)

        private_key_k2 = random.randint(1000, 10000)
        print("Jevon Private Key (Xb): ", private_key_k2, '\n')
    
    # Definition: Compute the sahred secret key
    # Parameters: Public keys (int) of each participant 
    # Returns: Shared private key (int)
    def compute_secret(public_key_k1, public_key_k2):
        global private_key_k1, private_key_k2, prime_q
    
        print("Exchanging the public keys | Alex's public key <---> Jevon's public key\n")

        print("Calculation of secret key by User A (K = (Yb ^ Xa) mod q)")
        print("Calculation of secret key by User B (K = (Ya ^ Xb) mod q)\n")

        print("Alex's secret key (Ka) = Yb ^ Xa mod q")
        print(" " * 23 + "=", public_key_k2, "^", private_key_k1, " mod ", prime_q, '\n')

        print("Jevon's secret key (Kb) = Ya ^ Xb mod q")
        print(" " * 24 + "=", public_key_k1, "^", private_key_k2, " mod ", prime_q, '\n')

        # Swapping the Public Keys to generate the Secret Key
        shared_secret_k1 = pow(public_key_k2, private_key_k1) % prime_q
        shared_secret_k2 = pow(public_key_k1, private_key_k2) % prime_q

        # If the secret keys are properly shared, return that key
        if (shared_secret_k1 == shared_secret_k2):
            print("Shared Secret Key:", shared_secret_k1)
            return shared_secret_k1
        else:
            print("Error: An issue occurred generating the shared key")
            return -1
    
    # Definition: Calculate the GCD of two integers
    # Parameters: int a, int b
    # Returns: Greatest common divisor of a and b (int)
    def gcd(a, b):
        while b!=0:
            a, b = b , a % b
        return a
    
    # Definition: Generates a list of prime numbers within lower and upper bounds
    # Parameters: int lower, int upper 
    # Returns: A list of all prime numbers between lower and upper bounds 
    def gen_primeNumber(lower, upper):
        # Loop through all numbers in specified range
        for num in range(lower, upper + 1):
           if num > 1:
               # Check if num is divisible by any number from 2 to num - 1
               for i in range(2, num):
                   # If num is divisible by any number, it is not prime 
                   if (num % i) == 0:
                       break
               else:
                   # If loop completes without finding a divisor for num, num is prime - append to list
                   primeSet.append(num)

    # Definition: Generate the public keys for each participant
    # Parameters: N/A
    # Returns: Two public keys - int x, int y
    def gen_publicKey():
        global private_key_k1, private_key_k2, G, prime_q
        primitive = []
        print("Calculate public keys:\n")
        
        # Picks Random Prime q
        prime_q = pick_random_prime()

        # Generates an Array of Primitive Roots of prime q
        primitive = primitiveRoot(prime_q) 

        # Generating Random Iterator to select from Primitive Array
        j = random.randint(0, len(primitive) - 1)

        # Assigns G to a Random Primitive Root of prime_q
        G = primitive[j]

        print("Random prime number q =", prime_q)
        print("Random primitive root of q (variable G) =", G)

        print("\nAlex's public key (Ya) = (G ^ Xa) mod q")
        print(" " * 23 + "=", G, "^", private_key_k1, " mod ", prime_q)

        # Generate Alex's public key 
        x = pow(G, private_key_k1) % prime_q 
        print(" " * 23 + "=", x, '\n')

        print("Jevon's public key (Yb) = (G ^ Xb) mod q")
        print(" " * 24 + "=", G, "^", private_key_k2, " mod ", prime_q)

        # Generate Jevon's public key
        y = pow(G, private_key_k2) % prime_q
        print(" " * 24 + "=", y, '\n')

        return x, y
    
    # Definition: Pick two random prime numbers from a list of primes
    # Parameters: N/a   
    # Returns: Prime number (int)
    def pick_random_prime():
        #Generating Random Iterator to select from Prime Array
        i = random.randint(0, len(primeSet) - 1)
        prime = primeSet[i]

        # Once a random prime is selected, remove that number from the set of primes
        primeSet.remove(prime)
        return prime

    # Definition: Generates a list of primitive roots for a given prime number
    # Parameters: A prime number (int) for which to find the primitive roots
    # Returns: List of primitive roots
    def primitiveRoot(prime_q):
        # Initialize  list of primitive roots to populate
        primitive_roots = []

        # Generate a set of integers between 1 and q - 1 that are coprime with q
        # These numbers are candidates for being primitive roots
        initial_set = set(num for num in range (1, prime_q) if gcd(num, prime_q) == 1)

        # Loop through all integers from 1 to q - 1 to check if they are primitive roots
        for g in range(1, prime_q):
            # For each candidate g, we generate a set of all its powers mod prime_q into root_set
            root_set = set(pow(g, power) % prime_q for power in range (1, prime_q))

            # if the set of powers of g (root_set) is the same as the set of coprimes (initial_set) then g
            # is able to generate all the integers that are coprime with prime_q, then g is a primitive root - add to list. 
            if initial_set == root_set:
                primitive_roots.append(g)
        
        # After iterating, return the list of primitive roots
        return primitive_roots

    print("Diffie–Hellman Key Exchange!", '\n')

    # Initialize list of primes
    primeSet = []

    # Generate private keys for Jevon & Alex
    assign_private_key()
    
    # Generate a prime number between a lower and upper bound 
    gen_primeNumber(0, 1000)

    # Generate public keys for Jevon & Alex 
    public_key_k1, public_key_k2 = gen_publicKey()

    # Compute the secret key, given both public keys
    secret = compute_secret(public_key_k1, public_key_k2) 

runDH()