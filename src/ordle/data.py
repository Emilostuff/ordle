import os
from os.path import exists
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


def _extract_words(data, length, alphabet):
    # returns all distinct, valid {length}-letter words
    valid = set()
    for line in data:
        word = line.split("\t")[0].upper()

        if not len(word) == length:
            continue

        if all(c in alphabet for c in word):
            valid.add(word)

    return list(valid)


def _fetch(url):
    response = urlopen(url)
    zipfile = ZipFile(BytesIO(response.read()))
    file = zipfile.infolist()[0]
    file.filename = "temp.txt"
    zipfile.extract(file)

    data = None
    with open("temp.txt") as f:
        data = f.read().splitlines()
    os.remove("temp.txt")

    return data


def get_words(length, alphabet):
    path = f"words{length}.txt"

    # check if local copy exists
    if exists(path):
        f = open(path)
        return f.read().splitlines()

    # otherwise download wordlist
    data = _fetch("https://korpus.dsl.dk/download/ddo-fullform.zip")

    # process wordlist
    words = _extract_words(data, length, alphabet)

    # save words
    with open(path, "w") as out:
        out.write("\n".join(words))

    return words


if __name__ == "__main__":
    get_words(5)
