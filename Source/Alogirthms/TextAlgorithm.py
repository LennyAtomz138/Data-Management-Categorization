"""
An algorithm that is intended to analyze plain text (as opposed to graphs and the like).
"""

from Source import TextractPDFDemo


class TextAlgorithm:

    def __init__(self, keyword):
        """
        Initialize TextAlgorithm class with a keyword for search.
        :param keyword: The value to be used in comparison operations.
        """
        self.num_match = 0
        self.keyword = keyword

    def find_num_matches(self):
        """
        Returns the number of keyword matches that were detected.
        :return:
        """
        # TODO: Configure this method to read the DocumentProcessor.text_array.
        while TextractPDFDemo.main() is not 0:
            # figure out how to read from string stream...
            pass
