# Analyzes text in a document stored in an S3 bucket. Display polygon box around text and angled text
import boto3
import io
import boto3
from io import BytesIO
import sys
import json
import time
from Source.Algorithms import TextAlgorithm

import math
from PIL import Image, ImageDraw, ImageFont

text_array = []

# Displays information about a block returned by text detection and text analysis
def DisplayBlockInformation(block):

    if 'Text' in block:
        print('    Detected: ' + block['Text'])
    print()


def ProcessDoc(bucket, document):
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
    print('Detected Document Text')

    # Create image showing bounding box/polygon the detected lines/text
    for block in blocks:
        StoreBlockText(block)
        #DisplayBlockInformation(block)

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


def Main(incoming_keywords):
    bucket = 'uconn-sdp-team11-unprocessed-docs'
    document = 'AWS-Achieves_FED-Ramp-JPEG.jpg'

    keywords = incoming_keywords

    #print("<TEST>: Here are the keywords:\n", keywords)

    block_count = ProcessDoc(bucket, document)

    find_matches = TextAlgorithm
    find_matches.find_num_matches(keywords, text_array)


if __name__ == "__main__":
    Main()