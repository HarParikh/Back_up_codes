import string


def remove_punctuation(text_file):
    """
    The input has to be a txt file.
    """
    text = open(text_file).read()
    return text.translate(str.maketrans("", "", string.punctuation))


def number_of_words(input_text_file):
    """
    The input has to be a txt file.
    """
    try:
        counts = {}
        for word in remove_punctuation(input_text_file).split():
            if word not in counts:
                counts[word] = 1
            else:
                counts[word] += 1
        for key, value in counts.items():
            print(f"The word {key} has appeared {value} times.")
    except:
        return "Invalid File"


if __name__ == "__main__":
    number_of_words("text_file.txt")
