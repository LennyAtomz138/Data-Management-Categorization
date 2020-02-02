"""
An algorithm that is intended to analyze plain text (as opposed to graphs and the like).
"""


class TextAlgorithm:
    """
    Used to parse documents in a specified S3 bucket for keyword matches.
    Initialized with keywords and a array of Textracted strings.
    """


def find_num_matches(keywords, text_array):
    """
    Returns the number of keyword matches that were detected.
    :param keywords: A list of keyword values.
    :param text_array: An array of Textracted strings.
    :return:
    """
    text_dictionary = {}
    for word in keywords:
        text_dictionary.update({word: 0})

    for word in text_array:
        if word in keywords:
            text_dictionary[word] += 1

    print("<TEST>: Number of observed matches: ", text_dictionary)