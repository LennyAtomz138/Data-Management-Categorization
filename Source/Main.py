"""
Main program loop
"""

import boto3
import textract  # This import may not be needed.

from Source import CLIMenu


# client = boto3.client('textract')  # This may be all that's needed to get Textract called within this file.

#  if __name__ == '__main__':

if __name__ == "__main__":
    CLIMenu.MainMenu()

# def main():
#     MainMenu()
