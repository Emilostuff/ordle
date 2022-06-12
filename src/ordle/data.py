
def get_words(data, length):
    # collect all valid {length}-letter words
    valid = []
    for line in lines:
        # discard ending
        x = line.split(";")[0]

        # keep only the first of dublets
        if x[0] == "1":
            x = x[3:]

        if not len(x) == length:
            continue

        if all(c in "abcdefghijklmnopqrstuvwxyzæøå" for c in x):
            valid.append(x.upper())

    return valid


if __name__ == '__main__':
    with open('dictionary.txt') as f:
        # get lines
        lines = f.readlines()

        # extract words
        words = get_words(lines, length=5)
        print(f"Selected {len(words)} words")

        # store output
        with open('words.txt', 'w') as f:
            f.write('\n'.join(words))
