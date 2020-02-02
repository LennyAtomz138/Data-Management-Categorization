"""
An algorithm that is intended to analyze plain text (as opposed to graphs and the like).
"""


# TODO: Ensure that this class is called with a list of keywords and the DocumentProcessor.text_array!
class TextAlgorithm:
    """
    Used to parse documents in a specified S3 bucket for keyword matches.
    Initialized with keywords and a array of Textracted strings.
    """
    def __init__(self, keywords, text_array):
        """
        Initialize TextAlgorithm class with a keyword for search.
        :param keywords: A list of keyword values.
        :param text_array: An array of Textracted strings.
        """
        # self.num_match = 0
        self.keywords = keywords
        self.text_array = text_array
        self.text_dictionary = {}

        for word in self.keywords:
            self.text_dictionary.update({word: 0})

    # TODO: Configure method to annotate how many times each keyword was detected.
    # TODO: -> Use a dictionary to keep a tally of each occurrence
    def find_num_matches(self):
        """
        Returns the number of keyword matches that were detected.
        :return:
        """
        for word in self.text_array:
            if word in self.keywords:
                self.text_dictionary[word] += 1

        print("<TEST>: Number of observed matches: ", self.text_dictionary)
