"""
FolderHandle handles the Initial, Untagged, and Tagged folders.
Initial: Used to store files as soon as the tool launches.
Untagged: Used to store files that were NOT tagged during analysis (i.e.; No keyword(s) detected).
Tagged: Used to store files that WERE tagged during analysis (i.e.; Keyword(s) detected).
"""

# TODO: Create method that creates a folder named after the keyword passed to it.
# TODO: Modify the above method to create permutations of keyword folders when
#  more than one tag is present for a given doc.
# TODO: Create method that places the tagged documents into their respective folders.
# TODO: Create method that sends the folders to respective S3 buckets in AWS upon completion.


class FolderHandle:
    """A class that is used to manage the various types of folders.
    Note that (currently) all lists will be shared by all instances of the FolderHandle class."""

    initial = []
    untagged = []
    tagged = []

    def add_to_initial(self, file):
        """Class method that adds a file to the Initial Folder."""
        self.initial.append(file)
        return

    def add_to_untagged(self, file):
        """Class method that adds a file to the Untagged Folder."""
        self.untagged.append(file)
        return

    def add_to_tagged(self, file):
        """Class method that adds a file to the Tagged Folder."""
        self.tagged.append(file)
        return
