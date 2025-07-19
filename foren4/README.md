# 諸葛亮

## Description

Shane is working on making NDNs (Nerdy Dinosaur Names). It seems the data in the files have been stored weirdly. Can you help?

## Flag

`wxmctf{TyrannoTechnoTinkerer}`

## Solution

Every four bytes of the zip file have been flipped from little-endian to big-endian. 

After extracting the zip, the first two bytes and last two bytes of every four-byte chunk in the file have been separated. 