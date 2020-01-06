"""
FolderHandle handles the Initial, Untagged, and Tagged folders.
Initial: Used to store files as soon as the tool launches.
Untagged: Used to store files that were NOT tagged during analysis (i.e.; No keyword(s) detected).
Tagged: Used to store files that WERE tagged during analysis (i.e.; Keyword(s) detected).
"""


class FolderHandle:
    """A class that is used to manage the various types of folders."""

    initial = []
    untagged = []
    tagged = []

    def add_to_initial(self):
        pass

    def add_to_untagged(self):
        pass

    def add_to_tagged(self):
        pass

    pass
