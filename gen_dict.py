#!/usr/bin/env python

import string
import sys

def clean_dict(original, dest):
    cleaned_words = set()
    valid_letters = set(string.ascii_lowercase + string.ascii_uppercase)

    with open(original) as f:
        for line in f.read().split("\n"):
            valid = True

            for char in line:
                if char not in valid_letters:
                    valid = False
                    break

            if not valid:
                continue

            cleaned_words.add(line.lower())
                    
    with open(dest, "w") as f:
        f.write("\n".join(sorted(cleaned_words)))


if __name__ == "__main__":
    clean_dict(sys.argv[1], sys.argv[2])
