import random
import math
from hashlib import sha1
from sympy import isprime

# dependencies: sympy (pip install sympy) - for prime number checking

# Program for digitally signing using the Digital Signature Algorithm (DSA)
# Part of CPSC 3730 Project

# place program under function runDSA so it can be called by GUI 
def runDSA():
    # Definition: Function to compute the parameters p and q. Complies with Digital Signature Standard (DSS) requirements
    # Parameters: L and N need to be defined
    # Returns: p and q
    def compute_P_Q():
        # N specifies the bit length of prime number q

        # variable decies number of iterations for generating p. Divides generation process in multiple steps
        iterationsForPCalc = math.floor((L - 1) / N)
        
        # number of remaining bits after dividing L - 1 by g
        # used for determining size of last block when constructing p, ensures p is within the range 2^L-1 < p < 2^L
        sizeOfLastBlock = (L - 1) % N
        
        # returns computed value for q and random number s used for q's generation, and needs to be used for p's generation
        q, s = compute_Q()

        # Iterate until valid p found
        while True:
            # generate some random j between 0 and 2^(N-1), used in hash computation, generates more randomness
            randomJ = random.randint(0, pow(2, N - 1)) 
            
            # V holds valid hash values to be used in generating P
            V = []
            for _ in range(iterationsForPCalc + 1):
                # Generate a random value for k to introduce additional randomness
                randomK = random.randint(0, pow(2, N - 1)) # generate some random k as well  

                # Compute hash using s, j, and k.
                hashResult = processSha1(s + randomJ + randomK)
                hashed = int.from_bytes(hashResult.digest(), byteorder='big')
                # convert hash from hex to integer and store in V
                V.append(hashed)

            # W combines the hash values of V into one value
            WSum = []
            
            # calculate part of value for W
            # W will contribute to calculation of p and as such needs to be random, and un-biased 
            for i in range(iterationsForPCalc):
                WCalc = V[i] * pow(2, (160 * i))
                WSum.append(WCalc)

            # next part in calculating W
            WSum.append((V[iterationsForPCalc] % (pow(2, sizeOfLastBlock))) * (pow(2, N * iterationsForPCalc)) + (2 ** (L - 1)))

            # let W be the sum of each index in WSum
            W = sum(WSum)

            # calculate remainder of w mod 2 * q
            remainder = W % (2 * q)

            # finally, calculate p
            p = (W - remainder) + 1

            # assert is_prime(q), "q is NOT prime"
            # assert ((p - 1) % q == 0), "q NOT prime divisor of (p - 1)"

            # ensure that p meets all requirements: 
            # p must be prime
            # 2^L-1 < p < 2^L
            # q must be prime divisor of (p - 1) 
            if p >= 2 ** (L - 1) and isprime(p) and isprime(q) and ((p-1) % q == 0):
                return p, q

    # Definition: Turns passed parameter into bytes and passes to sha1 functin
    # Parameters: integer param
    # Returns: SHA1 hash
    def processSha1(param):
        # calculate number of bits required to turn param into bytes
        lengthOfParam = math.floor((param.bit_length() + 7) / 8)

        # turn s into bytes so sha1 will accept it
        paramInBytes = param.to_bytes(lengthOfParam, 'big')

        # apply sha1 to s
        paramWithSha1 = sha1(paramInBytes)

        return paramWithSha1

    # Definition: Function for calculating the parameter q
    # Parameters: L and N need to be defined
    # Returns: paramter q and a random variable s
    def compute_Q(): 
        # Generate q
        while True:
            # summary: Computing q as per process outlined in Digital Signature Standard
            #          compute random number s, apply SHA-1
            #          compute z, remainder of random number s+1 % 2^N, apply SHA-1 
            #          XOR s and z
            #      
            #          if q is prime: accept, else: loop continues 
            
            # compute random seed value between 1 and 2^N
            sRandom = random.randrange(1, pow(2, N))
            
            # apply SHA1 to s
            sWithSha1 = processSha1(sRandom)

            # zRemainder is the remainder of sRandom + 1 mod 2^N
            zRemainder = (sRandom + 1) % pow(2, N)

            # apply SHA1 to zRemainder
            zWithSha1 = processSha1(zRemainder)
        
            # Convert z and s back to integers after applying sha1
            sWithSha_int = int.from_bytes(sWithSha1.digest(), byteorder='big')
            zWithSha_int = int.from_bytes(zWithSha1.digest(), byteorder='big')

            # XOR seed s and z 
            q = sWithSha_int ^ zWithSha_int

            # ensure q is prime, accept q if prime, and q must be 2^N-1 < q < 2^N, otherwise loop continues n   
            if isprime(q) and (q > pow(2, N - 1)) and (q < pow(2, N)):
                return q, sRandom

    # Definition: Function for calculating the parameter g
    # Parameters: takes parameter p and q
    # Returns: parameter g
    def compute_G(p, q):
        flag = True

        # loop until g is greater than 1
        while flag == True:
            # h is any integer greater than 1, and less than p-1
            h = random.randrange(2, p - 1) 
            
            # calculate the floor of exponent to which h is raised & ensure it is an integer.
            # g = h^(p-1)/q mod p
            pFloorq = ((p - 1) // q)
            g = pow(h, pFloorq, p)
        
            # make sure g calculation is greater than 1
            if g > 1:
                flag = False
        
        return g

    # Definition: Function returns the signature parameters r and s
    # Parameters: takes p, q, g, user's private key (x), and the message (M)
    # Returns: parameter r and s
    def signing(p, q, g, x, M):
        # make sure p and q are prime 
        assert isprime(p), "p parameter is not prime"
        assert isprime(q), "q parameter is not prime"
        # assert (pow(g, q, p) > 1 and g > 1 and p - 1 % q)
        
        print("Message M to digitally sign: ", end="")
        print(M.decode())

        print(f"\n   User's private key is: {x}")

        while True: 
            k = random.randint(1, q - 1) # generate a random integer such that 0 < k < q
            r0 = pow(g, k, p) # calculate r as (g^k mod p) mod q
            r = r0 % q
            M = int(sha1(M).hexdigest(), 16) # calculate the hash of M using SHA-1
        
            # ensure k isn't 0
            if k == 0:
                continue
            
            # Invert k and mod q to make sure k is 0 < k < q 
            kInverted = pow(k, -1, q)
            
            # ensure when k is inverted, there is a valid result
            if kInverted is None: 
                continue 
                
            # calculate s parameter
            s = (kInverted * (M + (x * r))) % q

            print("   \n   Output of Signing function: ")
            print("   r value of signature: ", end="")
            print(r)
            print("   s value of signature: ", end="")
            print(s)
            print()

            return r, s

    # Definition: Verifies the digital signature
    # Parameters: takes p, q, g, the received message (M), user's public key (y), and signing parameters (r and s)
    # Returns: True or False
    def verifying(p, q, g, M, y, r, s):
        assert isprime(p), "p parameter is not prime"
        assert isprime(q), "q parameter is not prime"
        assert (pow(g, q, p) == 1 and (g > 1) and p - 1 % q), "Issue with parameters"

        # calculate w   
        # invert s and modulus by q
        w = pow(s, -1, q)

        # shrink m so it can fit into index-sized integer
        hashMReceived = int(sha1(M).hexdigest(), 16)

        # calculate u1, u2 parameters
        u1 = (hashMReceived * w) % q 
        u2 = (r * w) % q

        # calculate v
        # v = [(g^(u1) * y^(u2)) mod p ] mod q
        v = (pow(g, u1, p) * pow(y, u2, p)) % p % q
        
        # if v is equal to r, digital signature is verified
        # otherwise, digital signature not verified
        print(f"\n   The value of v is: {v}\n", end="")
        print(f"   The value of r is: {r}\n\n", end="")

        test = (v == r)
        print(f"   v == r: {test}")
        return v == r

    # Initialize values..

    L = 1024 # L is a bit length between 512 and 1024 (inclusive) used for controlling the length of prime number p
    N = 160 # N specifies the bit length of prime number q

    # Global public-key components
    p, q = compute_P_Q()
    g = compute_G(p, q)

    # calculate User's Private Key (x)
    x = random.randint(1, q - 1)

    # calculate User's Public Key (y)
    y = pow(g, x, p)

    # sample input
    textInput = "I, Jevon, agree to the stipulations of this contract."

    # Encode message to be signed
    M = str.encode(textInput, 'ascii')

    # Signing the message
    r, s = signing(p, q, g, x, M)

    # Print statements and call verifying to check if signature is valid
    print(f"   Verify M's digital signature: ", end="")
    if verifying(p, q, g, M, y, r, s):
        print("   Digital signature IS valid\n")
    else:
        print("   Digital signature IS NOT valid\n")

    # Try another messsage, encode message to be signed
    textInput2 = "Yes, I have received the package. -Alex"
    M2 = str.encode(textInput2, 'ascii')

    # calculate user's private key
    x2 = random.randint(1, q - 1)

    # calculate User's Public Key (y)
    y2 = pow(g, x2, p)

    # get signing parameters
    r2, s2 = signing(p, q, g, x2, M2)

    # Print statements and call verifying to check if signature is valid
    print("   Verify M2's digital signature: ", end="")
    if verifying(p, q, g, M2, y2, r2, s2):
        print("   Digital signature IS valid\n")
    else:
        print("   Digital signature IS NOT valid\n")

    # Print statements to illustrate example of a possible attacker 
    print("SCENARIO:\n\n   An attacker successfully executes a replay attack and gets both the message and the signature data. ")
    print("   They now send an altered message to the receiver, does DSA verify the signature?\n")
   
    # attacker encodes a different message
    textInput3 = "Send bitcoin to this address or face consequences 1A1zP1eP5QGefi2DMPTfT"
    M3 = str.encode(textInput3, 'ascii')

    print(f"   Original message: {M2.decode()}")
    print(f"   Captured parameter r is: {r2}")
    print(f"   Captured parameter s is: {s2}")
    print(f"   Attacker's new message: {M3.decode()}\n")
    print("   Verify M3's digital signature: ", end="")

    # attacker tries to pass different message using intercepted parameters, check if verifying validates signature
    if verifying(p, q, g, M3, y2, r2, s2):
        print("   Digital signature IS valid\n")
    else:
        print("   Digital signature IS NOT valid\n")

# For running entire program, entire program bundled under this function for GUI implementation
runDSA()



