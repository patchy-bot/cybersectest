# Covert Chinchillas

## Description

Everyone knows that eatingfood loves his chinchilla. In fact, all he ever does is send pictures of his chinchilla! However, something doesn't seem right. These adorable photos could have a secret waiting to be revealed...

## Flag

`wxmctf{7h1n95_423_n07_41w4y5_wh47_7h3y_533m}`

## Solution

Look through the image's metadata to find a password encrypted in base 64. The password is then used to extract the flag, which is hidden with LSB steganography. Steghide or any other similar tools should be enough to get the flag.
