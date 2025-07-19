# Notepad++ Development

Distribute checker.txt, everything else is source files and solutions in case something breaks.

## Description

Timmy is a little insane. He prefers to write his flag checkers in Notepad++. Unfortunately for the rest of us, he forgot to translate it back into a normal binary. Can you figure out how his flag checker works?

## Flag

wxmctf{G0d_D4mm1t_T1mmy}

## Solution

Run `assemble.py` (plz ignore my shitty python code). It converts the text file back into a binary. The checker just inverts all the bits in the flag, and compares against an array of shorts.

***

In case something breaks, the tee-binary.sh script can be used to write the hexdump of a binary to a text file. The source for the checker, and compiled binary are also included in to `do-not-distribute` directory.
