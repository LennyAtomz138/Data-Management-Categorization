# Analyzes text in a document stored in an S3 bucket. Display polygon box around text and angled text
import boto3
import io
from io import BytesIO
import sys

import math
from PIL import Image, ImageDraw, ImageFont


# Displays information about a block returned by text detection and text analysis
def DisplayBlockInformation(block):

    if 'Text' in block:
        print('    Detected: ' + block['Text'])

    print()


def process_text_analysis(bucket, document):
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

        DisplayBlockInformation(block)

    return len(blocks)


def main():
    bucket = ''
    document = ''
    block_count = process_text_analysis(bucket, document)
    print("Blocks detected: " + str(block_count))


if __name__ == "__main__":
    main()