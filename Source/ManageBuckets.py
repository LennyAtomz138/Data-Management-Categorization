"""
ManageBuckets is used to view, move, and delete file objects from within a specified AWS S3 bucket.
List of boto3 methods: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
List of s3api commands: https://docs.aws.amazon.com/cli/latest/reference/s3api/#description
"""

import boto3

# A low-level client representing Amazon Simple Storage Service (S3)
client = boto3.client('s3')


# TODO: Ensure that the file object KEY is passed as the filename.
def MoveFile(self, filename, source_bucket, destination_bucket):
    """
    This function moves files from source bucket to destination bucket.
    :param self:
    :param filename: AWS key of file object to be moved
    :param source_bucket: original location of the file object
    :param destination_bucket: intended destination for the file object
    :return:
    """
    self.filename = filename
    self.source_bucket = source_bucket
    self.destination_bucket = destination_bucket

    src_bucket_object = client.get_object(
        Bucket=source_bucket,
        Key=filename
    )

    dst_bucket_object = client.put_object(
        Bucket=destination_bucket,
        #Key=filename
        Key=src_bucket_object.Key
    )


def ViewFile():
    pass


def ChooseFilesToScan():
    pass
