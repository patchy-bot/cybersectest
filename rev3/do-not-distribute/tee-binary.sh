#!/bin/bash
echo ./$1
hexdump -Cv ./$1 > $2
