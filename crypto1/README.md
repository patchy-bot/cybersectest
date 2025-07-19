# Common Faults

**do not distribute solve.py, server is needed to host the program**

## Description
lostcactus has a gold vault, but is faulty, so to protect his gold, he encrypted the password with RSA. lostcactus, a fond fan of Euler, generated a list of public keys, until it contained `271828`, the first 6 digits of Euler's number.
Unfortunatly for lostcactus, just like his vault, his key generator is also faulty, having a COMMON issue with his vault. Help him find his password again.

## Flag
`wxmctf{CommOn_F@u1t_0R_cOMm0N_f4ctoR?}`

## Solution
Run `solve.py`, it takes the common factors of the public keys to find the prime factors to then decrypt the ciphertext