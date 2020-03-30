"""
ManageBuckets is used to view, move, and delete file objects from within a specified AWS S3 bucket.
List of boto3 methods: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
List of s3api commands: https://docs.aws.amazon.com/cli/latest/reference/s3api/#description
"""

import boto3

# A low-level client representing Amazon Simple Storage Service (S3)
client = boto3.client('s3')

practice_src_bucket = 'uconn-sdp-team11-unprocessed-docs'
practice_object = 'Test3PagePDF_Seven_Ways_to_Apply_the_Cyber_Kill_Chain_'\
                  'with_a_Threat_Intelligence_Platform-page-003.pdf'
practice_dst_bucket = 'uconn-sdp-team11-tagged-docs'


# TODO: Ensure that the file object KEY is passed as the filename.
def MoveCopiedFile(filename, source_bucket, destination_bucket):
    """
    This function copies file from source bucket to destination bucket.
    :param filename: AWS key of file object to be moved
    :param source_bucket: original location of the file object
    :param destination_bucket: intended destination for the file object
    :return:
    """

    get_object_response = client.get_object(
        Bucket=source_bucket,
        Key=filename
    )

    put_object_response = client.put_object(
        Bucket=destination_bucket,
        Key=filename
    )

    return get_object_response, put_object_response


def ViewBucketFiles(bucket):
    """
    Creates a dictionary of S3 file objects that are found within 'bucket'.
    Prints a corresponding numbered list of those objects to the console.
    :param bucket: the S3 bucket of interest
    :return: dictionary of bucket items
    """
    j = 1
    file_titles = {}
    kwargs = {'Bucket': bucket}

    while True:
        i = 1
        response = client.list_objects_v2(**kwargs)
        for obj in response['Contents']:
            file_titles.update({i: obj['Key']})
            i += 1
        try:
            kwargs['ContinuationToken'] = response['NextContinuationToken']
        except KeyError:
            print("Encountered a KeyError while attempting to parse S3 bucket for file object keys.")
            break

    for title in file_titles:
        print(j, ":", file_titles[title])
        j += 1

    j = 0


def ChooseFilesToScan():
    pass


# TEST CODE BELOW:
#------------------------------------------------------------------#
# test_file_to_move = 'LM-White-Paper-Defendable-Architectures.pdf'
# MoveCopiedFile(filename=test_file_to_move,
#                source_bucket=practice_src_bucket,
#                destination_bucket=practice_dst_bucket)
#------------------------------------------------------------------#
# ViewBucketFiles(practice_src_bucket)
print("Made it this far.")
