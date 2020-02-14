"""
Class that handles all the individual files.
-> Holds all of the information that a file would have.
--> Filename, file doc_type, potential tags, etc.
"""
import string


class FileHandle:
    """A class that is used to manipulate (handle) the files themselves."""

    def __init__(self, name, filetype):
        self.fileName = name
        self.fileType = filetype
        self.tags = []

    def addtag(self, tag):
        self.tags.append(tag)
