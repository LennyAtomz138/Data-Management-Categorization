"""
An algorithm that is intended to analyze plain text (as opposed to graphs and the like).
"""


# TODO: Ensure that this class is called with a list of keywords and the DocumentProcessor.text_array!
class TextAlgorithm:

    def __init__(self, keywords, text_array):
        """
        Initialize TextAlgorithm class with a keyword for search.
        :param keywords: A list of keyword values.
        :param text_array: An array of Textracted strings.
        """
        self.num_match = 0
        self.keywords = keywords
        self.text_array = text_array

    def find_num_matches(self):
        """
        Returns the number of keyword matches that were detected.
        :return:
        """
        for word in self.text_array:
            if word in self.keywords:
                self.num_match += 1

        print("TEST: Number of observed matches: ", self.num_match)
        print("\n")
