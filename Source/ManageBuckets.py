"""
ManageBuckets is used to view, move, and delete file objects from within a specified AWS S3 bucket.
List of boto3 methods: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
List of s3api commands: https://docs.aws.amazon.com/cli/latest/reference/s3api/#description
"""

import boto3

# A low-level client representing Amazon Simple Storage Service (S3)
client = boto3.client('s3')

practice_src_bucket = 'uconn-sdp-team11-unprocessed-docs'
practice_object = 'Test3PagePDF_Seven_Ways_to_Apply_the_Cyber_Kill_Chain_with_a_Threat_Intelligence_Platform-page-003.pdf'
practice_dst_bucket = 'uconn-sdp-team11-tagged-docs'


# TODO: Ensure that the file object KEY is passed as the filename.
def MoveFile(filename, source_bucket, destination_bucket):
    """
    This function moves files from source bucket to destination bucket.
    :param filename: AWS key of file object to be moved
    :param source_bucket: original location of the file object
    :param destination_bucket: intended destination for the file object
    :return:
    """
    filename = filename
    source_bucket = source_bucket
    destination_bucket = destination_bucket

    src_bucket_object_response = client.get_object(
        Bucket=source_bucket,
        Key=filename
    )

    dst_bucket_object_response = client.put_object(
        Bucket=destination_bucket,
        Key=filename
    )

    return src_bucket_object_response, dst_bucket_object_response


def ViewFile():
    pass


def ChooseFilesToScan():
    pass


# TEST CODE BELOW:
test_file_to_move = 'LM-White-Paper-Defendable-Architectures.pdf'
MoveFile(filename=test_file_to_move,
         source_bucket=practice_src_bucket,
         destination_bucket=practice_dst_bucket)
print("Made it this far.")
