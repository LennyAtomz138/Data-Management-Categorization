"""
ManageBuckets is used to view, move, and delete file objects from within a specified AWS S3 bucket.
List of boto3 methods: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
List of s3api commands: https://docs.aws.amazon.com/cli/latest/reference/s3api/#description
"""

import boto3
from Source import CLIMenu, ExcelManager

# A low-level client representing Amazon Simple Storage Service (S3)
client = boto3.client('s3')


def ViewBuckets():
    """
    Prints all buckets that are accessible by current user.
    Calls SelectBucket() afterwards.
    :return: list of currently accessible buckets
    """
    list_bucket_response = client.list_buckets()
    bucket_number = 1
    bucket_titles = {}

    for item in list_bucket_response['Buckets']:
        bucket_titles.update({bucket_number: item['Name']})
        bucket_number += 1

    print("*=*" * 14)
    print("\t", " Numbered Bucket List")
    # print("\t\t  Numbered Bucket List")
    print("*=*" * 14)
    bucket_number = 1
    for title in bucket_titles:
        print(bucket_number, ":", bucket_titles[title])
        bucket_number += 1

    SelectBucket(bucket_titles)


def SelectBucket(bucket_list):
    """
    Enables user to select a bucket from within a list of user-accessible buckets.
    :param bucket_list: list of user-accessible buckets
    :return:
    """
    bucket_options = bucket_list

    # Prompt user to select a bucket number.
    while True:
        user_input = int(input("\nEnter Bucket Number: "))
        if user_input < 0 or user_input > len(bucket_options):
            print("Invalid input: Please try again.")
            continue
        else:
            CLIMenu.current_bucket = bucket_options[user_input]
            print("\nCurrent Bucket:")
            print(bucket_options[user_input], "\n")
            break

    # Once user has selected bucket, launch bucket file viewer (ViewBucketFiles()).
    while True:
        print("Would you like to proceed?\n")
        print("1 - Okay to Proceed")
        print("0 - Go Back\n")
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 1:
            print("Invalid input: Please try again.")
            continue
        elif ok_to_exit == 0:  # Go Back
            break
        elif ok_to_exit == 1:  # Okay to Proceed
            # If user has not selected a filename, prompt them to do so.
            if CLIMenu.selected_filename is None:
                ViewBucketFiles(CLIMenu.current_bucket)
            # Otherwise, user has a filename selected and they're ready to input keywords.
            else:
                CLIMenu.GetUserKeywords()
        else:
            continue


def ViewBucketFiles(bucket):
    """
    Creates a dictionary of S3 file objects that are found within 'bucket'.
    Prints a corresponding numbered list of those objects to the console.
    :param bucket: the S3 bucket of interest
    :return:
    """
    file_number = 1
    file_titles = {}
    kwargs = {'Bucket': bucket}
    list_objects_v2_response = client.list_objects_v2(**kwargs)

    # List out the bucket files, if it's empty launch new instance of bucket viewer (ViewBuckets()).
    while True:
        try:  # If bucket contains contents, print them out.
            for file_object in list_objects_v2_response['Contents']:
                file_titles.update({file_number: file_object['Key']})
                file_number += 1
            break
        except KeyError:  # If bucket is empty launch ViewBuckets().
            print("\nIt appears that the selected bucket is currently empty.")
            print("Please try again:\n")
            ViewBuckets()

    # Reset file_number for re-use here.
    file_number = 1
    print("")
    print("*=*" * 14)
    print("\t\t  Current Bucket Files")
    print("*=*" * 14)

    # Print out all bucket files.
    for title in file_titles:
        print(file_number, ":", file_titles[title])
        file_number += 1

    # Launch bucket file selector with the dictionary of file titles.
    SelectBucketFile(file_titles)


def SelectBucketFile(viewed_file_titles):
    """
    Assigns CLIMenu.selected_filename based on the file selected by the user.
    :param: viewed_file_titles: dictionary of file titles found within current bucket
    :return:
    """

    # Note that viewed_file_titles is a dictionary.
    file_titles = viewed_file_titles

    # Prompt user to select the file that they are interested in having analyzed.
    while True:
        print("\nPlease Select Option:")
        print("",
              "1 - Select Bucket File\n",
              "0 - Exit Bucket File Viewer\n")
        user_input = int(input("Enter Number: "))
        try:
            if user_input < 0 or user_input > 1:  # Repeat the options.
                print("Invalid input: Please try again.")
                continue
            elif user_input == 0:  # Leave this function call.
                print("Returning to the Main Menu")
                return
            elif user_input == 1:  # Identify the desired file by its corresponding file number.
                chosen_file_number = int(input("Enter the corresponding file number: "))
                if chosen_file_number < 1 or chosen_file_number > len(file_titles):
                    print("Invalid input: Please try again.")
                    continue
                else:  # Assign the global variable, CLIMenu.selected_filename, the file chosen by user.
                    chosen_file = file_titles[chosen_file_number]
                    CLIMenu.selected_filename = chosen_file
                    print("\nCurrent filename is now:\n", chosen_file, "\n")
                    return
        except ValueError:  # If some unanticipated value is encountered, retry.
            print("Encountered unexpected value error: Please try again.")
            continue
        else:  # If some other strange behavior takes place, break out of this loop.
            print("Encountered expected looping behavior: Exiting now.")
            break

    # Prompt user to decided whether or not to proceed with the keyword tagging process.
    while True:
        print("Proceed with Keyword Tagging?\n")
        print("",
              "1 - Proceed with Keyword Tagging\n",
              "2 - Select Different File\n",
              "0 - Return to Main Menu\n")
        ok_to_exit = int(input("Enter Number: "))
        try:
            if ok_to_exit < 0 or ok_to_exit > 2:
                print("Invalid input: Please try again.")
                continue
            elif ok_to_exit == 0:
                print("Exiting Bucket File Selector.")
                return
            elif ok_to_exit == 1:
                CLIMenu.GetUserKeywords()
            elif ok_to_exit == 2:
                ViewBucketFiles(CLIMenu.current_bucket)
        except ValueError:
            print("Encountered unexpected value error: Please try again.")
            continue


# TODO: Determine where to use this function.
# TODO: Will it be called in CLIMenu? If so, then when?
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

    if (get_object_response['ResponseMetadata']['HTTPStatusCode']) == 200:
        print("Successfully retrieved", filename, "from bucket", source_bucket, "\b.")
    else:
        print("Encountered error while attempting to retrieve",
              filename, "from bucket", source_bucket, "\b!")

    if (put_object_response['ResponseMetadata']['HTTPStatusCode']) == 200:
        print("Successfully moved a copy of", filename, "to bucket", destination_bucket, "\b.")
        ExcelManager.ModifyEntry(filename, source_bucket, destination_bucket)
    else:
        print("Encountered error while attempting to transfer a copy of ",
              filename, "from bucket", source_bucket, "to bucket", destination_bucket, "\b!")
    return


def DeleteOriginalFile(filename, original_bucket):
    """
    Deletes an S3 object file from its 'original bucket'.
    Intended to be used with MoveCopiedFile() such that it deletes the file that's in the source bucket.
    :param filename: the source file to be deleted
    :param original_bucket: the source bucket which contains the original file to be deleted
    :return:
    """
    response = client.delete_object(
        Bucket=original_bucket,
        Key=filename,
    )


# TODO: Note that it's currently configured to build a list of tags.
def TagFile():
    # TODO: Note that it's currently configured to build a list of tags.
    def add_tag(self, bucket, tags):
        self.tags.append(tags)
        self.bucket = CLIMenu.current_bucket

        response = client.put_object_tagging(
            Bucket=bucket,
            Key='Tag List',  # TODO: How does this key differ from the one(s) below?
            Tagging={
                'TagSet': [
                    {  # TODO: Will I pass in a dictionary here or just append one thing per request?
                        'Keyword': self.tags
                    }
                ]
            }
        )

    pass


# TEST CODE BELOW:
#------------------------------------------------------------------#
# import boto3
# client = boto3.client('s3')
# practice_src_bucket = 'uconn-sdp-team11-unprocessed-docs'
# practice_object = 'Test3PagePDF_Seven_Ways_to_Apply_the_Cyber_Kill_Chain_'\
#                   'with_a_Threat_Intelligence_Platform-page-003.pdf'
# practice_dst_bucket = 'uconn-sdp-team11-tagged-docs'
# test_file_to_move = 'LM-White-Paper-Defendable-Architectures.pdf'
# MoveCopiedFile(filename=test_file_to_move,
#                source_bucket=practice_src_bucket,
#                destination_bucket=practice_dst_bucket)
# test_file_to_delete = 'GSE63341_series_matrix.txt' <-- must upload prior to deletion test
#------------------------------------------------------------------#
# ViewBucketFiles(practice_src_bucket)
