from numpy import random
import tkinter as tk

def findWord():
    poss = []
    f = open('wordlist.txt', 'r')
    line = f.readline()
    while line:
        if len(line) == 8:
            if line[1] == 'r':
                if line[3] == 'i':
                    if line[5] == 'a':
                        if line[6] == 'r':
                            poss.append(line)
        line = f.readline().strip('\n')
    f.close()
    return poss

if __name__ == "__main__":
    print(findWord())