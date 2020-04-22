""" Analyzes text in a document stored in an S3 bucket. Can display polygon box around text and angled text. """

import io
import boto3
from Source import CLIMenu, FileHandle, ExcelManager, ManageBuckets
from Source.Algorithms import TextAlgorithm

import math
from PIL import Image, ImageDraw, ImageFont

text_array = []


def DisplayBlockInformation(block):
    """
    Displays information about a block returned by text detection and text analysis.
    :param block:
    :return:
    """
    if 'Text' in block:
        print('    Detected: ' + block['Text'])
    print()


def ProcessDoc(bucket, document):

    print("\nCurrently processing the requested document...")

    # Get the document from S3
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket, document)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    # Analyze the document
    client = boto3.client('textract')

    image_binary = stream.getvalue()
    response = client.analyze_document(Document={'Bytes': image_binary},
                                       FeatureTypes=["TABLES", "FORMS"])

    # Get the text blocks
    blocks = response['Blocks']
    width, height = image.size
    draw = ImageDraw.Draw(image)
    print('Successfully detected document text.\n')


    for block in blocks:
        StoreBlockText(block)

    return len(blocks)


def StoreBlockText(block):
    """
    Used to display information from within a Textract block.
    A Block represents items that are recognized in a document within a group of pixels close to each other.
    :param block: The item returned by Textract.
    :return:
    """
    if 'Text' in block:
        text_array.append(block['Text'].lower())


def Main(incoming_bucket, incoming_filename, incoming_keywords):
    # The goal is to have the bucket selected prior to this step.
    if incoming_bucket is None:
        bucket = 'uconn-sdp-team11-unprocessed-docs'
    else:
        bucket = incoming_bucket

    # The goal is to have the filename selected prior to this step.
    if incoming_filename is None:
        filename = 'AWS-Achieves_FED-Ramp-JPEG.jpg'
    else:
        filename = incoming_filename

    document = FileHandle.FileHandle(filename)
    keywords = incoming_keywords

    block_count = ProcessDoc(bucket, document.file_name)

    print("<TEST>: Here's the text array:\n", text_array)
    print("<TEST>: Here are the (sorted) keywords:\n", keywords)

    find_matches = TextAlgorithm
    text_dictionary = find_matches.find_num_matches(keywords, text_array)
    while True:
        print("Would you like to tag the scanned document?\n")
        print("1 - Okay to Proceed")
        print("0 - Quit to Main Menu\n")
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 1:
            print("Invalid input: Please try again.")
            continue
        elif ok_to_exit == 0:
            print("\n")
            return
        elif ok_to_exit == 1:  # Okay to Proceed
            tags = ExcelManager.AddEntry(text_dictionary)
            if (tags != 1):  # if there are tags to add, then add them
                ManageBuckets.TagFile(document, bucket, tags)
            return
        else:
            continue
