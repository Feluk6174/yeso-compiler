#!/bin/bash
yasm -f elf64 -g dwarf2 -o $1.o $1.asm
echo Compiled to $1.o
ld -o $1 $1.o
echo Linked to $1

if [ "$1" = "debug" ]
then
    echo "p (char[10])mem to primt memory"
    $1
fi

if [ "$1" = "run" ]
then
    $1
fi

