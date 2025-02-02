# CryptoTrio

## Project Description

This project demonstrates the implementation of three fundamental cryptographic algorithms - RSA (Rivest-Shamir-Adleman), DSA (Digital Signature Algorithm), and DH (Diffie-Hellman) - from scratch. The goal was to explore the core principles of public-key cryptography and secure communication by creating these algorithms without relying on pre-built cryptographic libraries.

This project was originally developed in collaboration with Alex Stephen as part of a Cryptography course at the University of Lethbridge. Moving forward, I plan to make incremental improvements to the code to enhance my understanding of cryptography and improve the utility of the project as a tool for visualizing and learning the fundamental concepts of encryption and cryptography.

### Dependencies 
sympy (pip install sympy) - for checking if a number is prime

## Algorithms implemented: 

### **RSA (Rivest-Shamir-Adleman)** 

RSA is a widely used asymmetric encryption algorithm that utilizes a public key for encryption and a private key for decryption. RSA is based on the prime factorization problem - the difficulty in factoring a large composite number into its prime factors. While multiplying two primes is easy and efficient, factorizing a large composite number is significantly more computationally challenging. This computational challenge underpins the security of RSA. 

### **DSA (Digital Signature Algorithm)**

DSA is primarily used for digital signatures, allowing a sender to sign a message, or document and prove that it is authentic. The recipient of the message can verify the signature using the sender's pubic key, which ensure that an attacker has not intercepted and modified the contents of the message. 

DSA's security is based on the Discrete Logarithm Problem, which involves the challenge of finding x (the private key) knowing y, g, and p where y = g^x (mod p). Essentially, we are trying to reverse the exponentiation to recover x, but doing so is computationally difficult. As such, this inherent difficulty forms the foundation of DSA's strong security. 

### **DH (Diffie-Hellman)**

Diffie-Hellman is a clever cryptographic protocol designed to securely exchange keys between two parties over an insecure communication channel. DH enables both parties to agree on a shared secrey key without directly transmitting it, ensuring that even if an attacker intercepts the communication, the secret key would not be compromised. 

Diffie-Hellman relies on the Discrete Logarithm Problem, which makes it computationally infeasible for an attacker to compute the shared secret key, even if they intercept public keys exchanged between the parties. DH is widely used in applications such as SSL/TLS for securing web traffic. 

## **Future Improvements**
Some of the improvements I intend to focus on include:

### **Optimizing Code Efficiency**: 
Streamlining the implementation for better performance.

### **Adding more encryption algorithms**: 
Expanding the project to include other well-known encryption algorithms, such as AES (Advanced Encryption Standard), DES (Data Encryption Standard), and ECC (Elliptic Curve Cryptography). This will allow for a broader comparison of different cryptographic techniques and their trade-offs in terms of security, efficiency, and use cases.

### **Enhancing Documentation**: 
Providing more detailed and clear explanations to make the code more understandable.

### **Upgrading the GUI**: 
Improving the user interface for a more visually pleasing and engaging experience.

### **Adding Interactive Features**: 
Allow users to add their own messages to encrypt. 
