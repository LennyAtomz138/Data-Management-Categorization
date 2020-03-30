"""
Class that handles all the individual files.
-> Holds all of the information that a file would have.
--> Filename, file doc_type, potential tags, etc.
"""
import string


class FileHandle:
    """A class that is used to manipulate (handle) the files themselves."""

    fileName = ""
    fileType = ""
    tags = []

    def __init__(self, name):
        self.fileName = name
        if self.fileName.endswith('.pdf'):
            self.fileType = 'pdf'
        elif self.fileName.endswith('.docx'):
            self.fileType = 'docx'
        else:
            raise TypeError("Filename: " + self.fileName +
                            "is not of type docx or pdf.  Please only use supported filetypes.")

    def addtag(self, tag):
        self.tags.append(tag)