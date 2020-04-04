"""
Class that handles all the individual files.
-> Holds all of the information that a file would have.
--> Filename, file doc_type, potential tags, etc.
"""

import boto3
from Source import CLIMenu

client = boto3.client('s3')


class FileHandle:
    """A class that is used to manipulate (handle) the files themselves."""

    file_name = ""
    file_type = ""
    bucket = ""
    tags = []

    def __init__(self, name):
        self.file_name = name
        if self.file_name.endswith('.pdf'):
            self.file_type = 'pdf'
        elif self.file_name.endswith('.docx'):
            self.file_type = 'docx'
        elif self.file_name.endswith('.jpg'):
            self.file_type = 'jpg'
        elif self.file_name.endswith('.png'):
            self.file_type = 'png'
        else:
            raise TypeError("Filename: " + self.file_name +
                            "is not of type docx or pdf.  Please only use supported filetypes.")

    # TODO: Note that it's currently configured to build a list of tags.
    def add_tag(self, bucket, tags):
        self.tags.append(tags)
        self.bucket = CLIMenu.current_bucket

        response = client.put_object_tagging(
            Bucket=bucket,
            Key='Tag List',  # TODO: How does this key differ from the one(s) below?
            Tagging={
                'TagSet': [
                    {  # TODO: Will I pass in a dictionary here or just append one thing per request?
                        'Keyword': self.tags
                    }
                ]
            }
        )
