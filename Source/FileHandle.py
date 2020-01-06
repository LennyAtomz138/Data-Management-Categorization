"""
Class that handles all the individual files.
-> Holds all of the information that a file would have.
--> Filename, file type, potential tags, etc.
"""
import string


class FileHandle:
    fileName = ""
    fileType = ""
    tags = []

    def __init__(self, name, filetype):
        self.fileName = name
        self.fileType = filetype

    def addtag(self, tag):
        self.tags.append(tag)
