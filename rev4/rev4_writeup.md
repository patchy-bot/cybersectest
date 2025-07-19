# Problem - **Recursive Combinatorics**
After effortlessly conquering Lifewrath's supposedly "hard" rev3 challenge, Acid went on a well-deserved three-week vacation. However, Lifewrath, salty about Acid's triumph, decided to create an even harder challenge for Acid — one that has Acid's least favorite topics: recursion and combinatorics.

Not wanting to use up all of Acid's vacation time, Lifewrath generously provided Acid with the following instructions:

## **The Challenge**
Contained within the file `rev4.py`, you'll find a Python function called `go()`. This function is your target.

Your mission is straightforward but far from simple: You need to determine the output of the `go` function when it's given the input of 1 trillion. Lets say this value is `a`

Once you've successfully calculated the value `a`, your next step is to use it to access a unique URL for accessing the rentry page. To do this, follow these steps:

- Calculate the SHA-512 hash of the result of `a XOR b`, where `b` is the first Mersenne prime with 157 digits.
- After obtaining the complete SHA hash, take the last 8 characters of this hash.
- Construct the rentry URL by appending these 8 characters to the base URL. For example, if the last 8 characters of the SHA hash are **28559d4f**, the rentry URL will be formed as: https://rentry.co/28559d4f.
- It's important to note that the specific rentry link provided (https://rentry.co/28559d4f) does not exist. Your calculated 8 characters will access a unique rentry page where the flag can be found.

Acid really didn't want to do this question, as he was on vacation. Can you help him do it?

****

# Writeup

- Difficulty: Hard
- Authors: Lifewrath and Acid (github: fireheartjerry)

The number we need to input is $500000000001$
The hash of it xor the mersenne is:
> a1dd6653e129112bc4cbf09bdda193b93cde2a1aab843d493d5dbf824a9997157bf100c321f1ba6053b53c2d2bdaf2587b235ca6e16a6e501231f251d8ea86ea

First mersenne prime with 157 digits is:
> 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151

****

### Engineer's Induction Proof of Functions (Should work for this problem)

- We first try figuring out the function `___(n,k)` . We can see that for small values of $n$ and $k$ , the function returns $n \cdot k$, so we can assume the function returns $n \cdot k$.

- Now, looking at `rock(a,n)`, we can see that by testing values of $n$ and $a$, we get that the function returns $a^n$, so we assume the function returns $a^n$.

- Looking at `paper(n)`, and at the key value pairs, for each key $i$, the value is the list `[(1<<i>>i)-1, 1<<i, (1<<i)<<1, ((1<<i)<<1)+(1<<i)]`.

    - We must first understand what the operators `<<` and `>>` mean:
        - `<<` is a bitwise/logical left shift, it shifts all the bits left, and the most significant bit is lost.
            1. `0010 << 1 = 0100`
            2. `0010 << 2 = 1000`
        - `>>` is a bitwise/logical right shift, it sifts all the bits right, and the least significant bit is lost.
            1. `1011 >> 1 = 0101`
            2. `1011 >> 3 = 0001`

    - For the purposes of this program, it suffices to assume that `x << y` is equivalent to $x \cdot 2^y$ and `x >> y` is equivalent to $\lfloor \frac{x}{2^y} \rfloor$.

    - Now we re-write each bitwise operation to a more readable form:
        - `(1<<i>>i) - 1 = 0`
        - `1<<i = 2**i`
        - `(1<<i)<<1 = 2 * 2**i`
        - `((1<<i)<<1)+(1<<i) = 3 * 2**i`

    - So the original obfuscated list is equivalent to `[0, 2**i, 2 * 2**i, 3 * 2**i]`, for all $0 \le i < n^n$.

- Now, looking at `scissors(n,a,x)`, we can see that it's repeatedly adding the remainders of $n \text{ mod } a$ to a list, which is the same as converting $n$ into base $a$. It also adds padding at the end, ensuring that the list has length x.

- In `go(n)`, for every $i$ from $0$ to $4^n - 1$, it writes it in base $4$.

    - Then, it multiplies each digit in the list by successive powers of 2, so we are converting from base 2 to base 10 (we extend the definitions of bases to include digits higher than the base).

    - Then, if this number in base $10$ is equal to $n$, we increase the count by $1$. This means that we're counting the total number of ways to convert a number to base $4$, and converting it from base $2$ to base $10$ to get n.

    - We only need $\lfloor \log_2n \rfloor + 1$ digits in the base 2 representation, so we need to only check numbers from 0 to $4^{\lfloor \log_2n \rfloor + 1} \le 16 \cdot 4^{\log_2n} \le 16n^2$.

    - Testing with small values, we can see that `go(n)` returns $\lfloor \frac{n}{2} \rfloor + 1$, meaning that we can guess our answer for $n = 10^{12}$ is $500000000001$, which works.

****

### Full and Rigourous Proof of Functions

- For `___(n,k)`, looking in the code, we see that `n&(1<<j)` will return $2^j$ if the binary representation of $n$ has a 1 at the $j + 1$ digit from the right, and 0 otherwise.

    - So, if $n = \overline{a_i a_{i-1} \dots a_{0}}\_{2}$, then we have `n&(1<<j)` will return $a_j \cdot 2^j$, meaning in one loop we have $a \text{ += } \Sigma_{k=0}^i (a_k \cdot 2^k) = n$.
 
        - Note that `&` is the bitwise AND operator, which compares each bit and returns `1` if both bits are `1` and `0` otherwise. Below is a truth table for bitwise AND:

            | x | y | x AND y |
            | --- | --- | :---: |
            | 0 | 0 |    0    |
            | 0 | 1 |    0    |
            | 1 | 0 |    0    |
            | 1 | 1 |    1    |

    - This proccess repeats $k$ times, so at the end we have $a = n$, and the process returns $n$.

- For `rock(a,n)`, we'll prove via induction.

    - For $n = 0$, we get that $a^0 = 1$, the output of the function.

    - Now, assume we have that $\text{rock(a, n) } = a^n$ for all $a$.

    - Now, `(2n+1)>>1 = n`, and `2n>>1 = n`, so `rock(___(a, a),(2n+1)>>1)` and `rock(___(a, a),2n>>1)` are both $a^{2n}$. (This can be proved using our above definitions of bitwise shifts).

    - Now, `2n&1 = 0`, so $\text{ rock(a, 2n) } = a^{2n}$, while `(2n+1)&1 = 1`, so $\text{rock(a, 2n+1)} = a^{2n+1}$.

    - Since every non-negative integer can be written in the form $2n$ or $2n + 1$, where $n \ge 0, n \in \mathbb{Z}$, we are done.

- For `go(n)`, we will prove this via generating functions.

    - Consider the polynomial $P(x) = \Pi_{k=0}^{\infty} \left(1 + x^{2^k} + x^{2\cdot 2^{k}} + x^{3\cdot 2^{k}}\right)$. Then, the coefficient of $x^n$ in the polynomial $P(x)$ is the number of ways to write $n$ in the form $\Sigma_{k=0}^{\infty} (a_k \cdot 2^k)$, where $a_k \in \{0,1,2,3\}$, which is exactly what the go function is computing.
    
    - From geometric series, we have that $1 + x^{2^k} + x^{2\cdot 2^{k}} + x^{3\cdot 2^{k}} = \frac{1 - x^{4 \cdot 2^k}}{1-x^{2^k}} = \frac{1 - x^{2^{k+2}}}{1-x^{2^k}}$.

    - Now, letting $b_k = 1-x^{2^k}$, we get that $P(x) = \Pi_{k=0}^{\infty} \frac{b_{k+2}}{b_k}$, which telescopes to $\frac{1}{b_0} \cdot \frac{1}{b_1}$.

    - From geometric sequences, we have that $\Sigma_{k=0}^{\infty} x^k = \frac{1}{1-x} = \frac{1}{b_0}$, and $\Sigma_{k=0}^{\infty} x^{2k} = \frac{1}{1-x^2} = \frac{1}{b_1}$. So, we have $P(x) = (1+x+x^2+\cdots)(1+x^2+x^4+\cdots)$.
    
    - Now, the coefficient of $x^n$ is the number of pairs of non-negative integers $(a,b)$ such that $2a + b = n$. Then, all solutions are of the form $(a, n - 2a)$. Now, $0 \le a$, and $0 \le n - 2a$, so $2a \le n$ and $a \le \frac{n}{2}$.

    - Since $a$ is an integer, we can say $a \le \lfloor \frac{n}{2} \rfloor$. Then, there are $\lfloor \frac{n}{2} \rfloor + 1$ pairs, and so the coefficient of $x^n$ is $\lfloor \frac{n}{2} \rfloor + 1$, which is the output of `go(n)`.

****

### Finishing Up

From the analysis, we do the respective hashes and eventually reach the rentry URL: https://rentry.co/d8ea86ea, opening it reveals our final flag for rev: `wxmctf{th4nk5_f0r_d01ng_r3v_4nd_by3}`.

Thanks for doing rev!

This problem was inspired through Problem 3 of the [BMO1 2021-2022 contest](https://bmos.ukmt.org.uk/solutions/bmo1-2022/).
