# TODO: Remove these 2 comments below this message when ready.
# Asynchronously processes text in a document stored in an S3 bucket.
# For set up information, see https://docs.aws.amazon.com/textract/latest/dg/async.html

import boto3
import botocore
import json
import sys
import time
from Source.Algorithms import TextAlgorithm
from Source import FileHandle
from Source import DOCXExtracter
from Source import CLIMenu
from Source import ExcelManager


class ProcessType:
    DETECTION = 1
    ANALYSIS = 2


class DocumentProcessor:
    jobId = ''
    textract = boto3.client('textract')
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')

    text_array = []

    roleArn = ''
    bucket = ''
    document = ''

    sqsQueueUrl = ''
    snsTopicArn = ''
    processType = ''

    def __init__(self, role, bucket, document):
        self.roleArn = role
        self.bucket = bucket
        self.document = document

    def ProcessDocument(self, doc_type):
        jobFound = False

        self.processType = doc_type
        validType = False

        # Determine which doc_type of processing to perform.
        if self.processType == ProcessType.DETECTION:
            response = self.textract.start_document_text_detection(
                DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}},
                NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})
            print('Processing doc_type: Detection')
            validType = True

        if self.processType == ProcessType.ANALYSIS:
            response = self.textract.start_document_analysis(
                DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}},
                FeatureTypes=["TABLES", "FORMS"],
                NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.snsTopicArn})
            print('Processing doc_type: Analysis')
            validType = True

        if validType is False:
            print("Invalid processing doc_type. Choose Detection or Analysis.")
            return

        print('Start Job Id: ' + response['JobId'])
        dotLine = 0
        while jobFound is False:
            sqsResponse = self.sqs.receive_message(QueueUrl=self.sqsQueueUrl, MessageAttributeNames=['ALL'],
                                                   MaxNumberOfMessages=10)

            if sqsResponse:

                if 'Messages' not in sqsResponse:
                    if dotLine < 40:
                        print('.', end='')
                        dotLine = dotLine + 1
                    else:
                        print()
                        dotLine = 0
                    sys.stdout.flush()
                    time.sleep(5)
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    textMessage = json.loads(notification['Message'])
                    print(textMessage['JobId'])
                    print(textMessage['Status'])
                    if str(textMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + textMessage['JobId'])
                        jobFound = True
                        self.GetResults(textMessage['JobId'])
                        self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                                ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(textMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    self.sqs.delete_message(QueueUrl=self.sqsQueueUrl,
                                            ReceiptHandle=message['ReceiptHandle'])

        # print('Done!')

    def CreateTopicAndQueue(self):

        millis = str(int(round(time.time() * 1000)))

        # Create SNS topic
        snsTopicName = "AmazonTextractTopic" + millis

        topicResponse = self.sns.create_topic(Name=snsTopicName)
        self.snsTopicArn = topicResponse['TopicArn']

        # create SQS queue
        sqsQueueName = "AmazonTextractQueue" + millis
        self.sqs.create_queue(QueueName=sqsQueueName)
        self.sqsQueueUrl = self.sqs.get_queue_url(QueueName=sqsQueueName)['QueueUrl']

        attribs = self.sqs.get_queue_attributes(QueueUrl=self.sqsQueueUrl,
                                                AttributeNames=['QueueArn'])['Attributes']

        sqsQueueArn = attribs['QueueArn']

        # Subscribe SQS queue to SNS topic
        self.sns.subscribe(
            TopicArn=self.snsTopicArn,
            Protocol='sqs',
            Endpoint=sqsQueueArn)

        # Authorize SNS to write SQS queue
        policy = """{{
          "Version":"2012-10-17",
          "Statement":[
            {{
              "Sid":"MyPolicy",
              "Effect":"Allow",
              "Principal" : {{"AWS" : "*"}},
              "Action":"SQS:SendMessage",
              "Resource": "{}",
              "Condition":{{
                "ArnEquals":{{
                  "aws:SourceArn": "{}"
                }}
              }}
            }}
          ]
        }}""".format(sqsQueueArn, self.snsTopicArn)

        response = self.sqs.set_queue_attributes(
            QueueUrl=self.sqsQueueUrl,
            Attributes={
                'Policy': policy
            })

    def StoreBlockText(self, block):
        """
        Used to display information from within a Textract block.
        A Block represents items that are recognized in a document within a group of pixels close to each other.
        :param block: The item returned by Textract.
        :return:
        """
        if 'Text' in block:
            self.text_array.append(block['Text'].lower())

    def DeleteTopicAndQueue(self):
        self.sqs.delete_queue(QueueUrl=self.sqsQueueUrl)
        self.sns.delete_topic(TopicArn=self.snsTopicArn)

    # Display information about a block

    def GetResults(self, jobId):
        maxResults = 1000
        paginationToken = None
        finished = False

        while not finished:

            response = None

            if self.processType == ProcessType.ANALYSIS:
                if paginationToken is None:
                    response = self.textract.get_document_analysis(JobId=jobId,
                                                                   MaxResults=maxResults)
                else:
                    response = self.textract.get_document_analysis(JobId=jobId,
                                                                   MaxResults=maxResults,
                                                                   NextToken=paginationToken)

            if self.processType == ProcessType.DETECTION:
                if paginationToken is None:
                    response = self.textract.get_document_text_detection(JobId=jobId,
                                                                         MaxResults=maxResults)
                else:
                    response = self.textract.get_document_text_detection(JobId=jobId,
                                                                         MaxResults=maxResults,
                                                                         NextToken=paginationToken)

            blocks = response['Blocks']
            print('Detected Document Text')
            print('Pages: {}'.format(response['DocumentMetadata']['Pages']))

            # Display block information
            for block in blocks:
                self.StoreBlockText(block)

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True

    def GetResultsDocumentAnalysis(self, jobId):
        maxResults = 1000
        paginationToken = None
        finished = False

        while not finished:

            response = None
            if paginationToken is None:
                response = self.textract.get_document_analysis(JobId=jobId,
                                                               MaxResults=maxResults)
            else:
                response = self.textract.get_document_analysis(JobId=jobId,
                                                               MaxResults=maxResults,
                                                               NextToken=paginationToken)

            # Get the text blocks
            blocks = response['Blocks']
            print('Analyzed Document Text')
            print('Pages: {}'.format(response['DocumentMetadata']['Pages']))

            # Display block information
            for block in blocks:
                self.StoreBlockText(block)

                if 'NextToken' in response:
                    paginationToken = response['NextToken']
                else:
                    finished = True


def Main(incoming_bucket, incoming_filename, incoming_keywords):
    """Runs Textract tool on document that is located in the specified AWS S3 bucket."""
    roleArn = 'arn:aws:iam::172734287275:role/aws-textract-role'

    # The goal is to have the bucket selected prior to this step.
    if incoming_bucket is None:
        bucket = 'uconn-sdp-team11-unprocessed-docs'
    else:
        bucket = incoming_bucket

    # The goal is to have the filename selected prior to this step.
    if incoming_filename is None:
        filename = 'An AWS Network Monitoring Comparison.docx'
    else:
        filename = incoming_filename

    document = FileHandle.FileHandle(filename)
    keywords = incoming_keywords

    if document.fileType == "pdf":
        analyzer = DocumentProcessor(roleArn, bucket, document.fileName)
        analyzer.CreateTopicAndQueue()
        analyzer.ProcessDocument(ProcessType.DETECTION)
        analyzer.DeleteTopicAndQueue()
        text_array = analyzer.text_array
    else:
        #TODO download file from AWS and get its local address
        s3 = boto3.resource('s3')
        tempfile = 'temp.docx'

        try:
            s3.Bucket(bucket).download_file(filename, tempfile)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        text_array = DOCXExtracter.extractDOCX(tempfile)


    # TODO: Comment out these <TEST> print statement when ready.
    print("<TEST>: Here's the text array:\n", text_array)
    print("<TEST>: Here are the (sorted) keywords:\n", keywords)

    # Call TextAlgorithm here and pass it the keywords and text_array.
    find_matches = TextAlgorithm
    text_dictionary = find_matches.find_num_matches(keywords, text_array)
    while True:
        print("\nWould you like to tag the scanned document?\n")
        print("1 - Okay to Proceed")
        print("0 - Quit to Main Menu\n")
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 1:
            print("Invalid input: Please try again.")
            raise ValueError
        elif ok_to_exit == 0:
            print("\n")
            #CLIMenu.MainMenu()
            break
        elif ok_to_exit == 1:  # Okay to Proceed
            ExcelManager.ExcelMenu(text_dictionary)

# TODO: Figure out how to keep Main Menu from launching after attempting to exit program,
#  note that this seems to happen after the Textractor does it job and the user is
#  returned to the Main Menu.
# if __name__ == "__main__":
#     Main()
