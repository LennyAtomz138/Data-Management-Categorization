"""
ManageBuckets is used to view, move, and delete file objects from within a specified AWS S3 bucket.
List of boto3 methods: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
List of s3api commands: https://docs.aws.amazon.com/cli/latest/reference/s3api/#description
"""

import boto3
from Source import CLIMenu

# A low-level client representing Amazon Simple Storage Service (S3)
client = boto3.client('s3')

practice_src_bucket = 'uconn-sdp-team11-unprocessed-docs'
practice_object = 'Test3PagePDF_Seven_Ways_to_Apply_the_Cyber_Kill_Chain_'\
                  'with_a_Threat_Intelligence_Platform-page-003.pdf'
practice_dst_bucket = 'uconn-sdp-team11-tagged-docs'


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
    print("\t\t  Numbered Bucket List")
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

    while True:
        user_input = int(input("\nEnter Bucket Number: "))
        if user_input < 0 or user_input > len(bucket_options):
            print("Invalid input: Please try again.")
            raise ValueError
        else:
            CLIMenu.current_bucket = bucket_options[user_input]
            print("\nCurrent Bucket:")
            print(bucket_options[user_input], "\n")
            break

    while True:
        print("Would you like to proceed?\n")
        print("1 - Okay to Proceed")
        print("0 - Try Again\n")
        ok_to_exit = int(input("Enter Number: "))
        if ok_to_exit < 0 or ok_to_exit > 1:
            print("Invalid input: Please try again.")
            raise ValueError
        elif ok_to_exit == 0:  # Try Again
            SelectBucket(bucket_options)
        elif ok_to_exit == 1:  # Okay to Proceed
            # If user has not selected a filename, prompt them to do so.
            if CLIMenu.selected_filename is None:
                ViewBucketFiles(CLIMenu.current_bucket)
            # Otherwise, user has a filename selected and they're ready to input keywords.
            else:
                CLIMenu.GetUserKeywords()


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
    while True:
        try:
            for file_object in list_objects_v2_response['Contents']:
                file_titles.update({file_number: file_object['Key']})
                file_number += 1
            break
        except KeyError:
            print("\nIt appears that the selected bucket is currently empty.")
            print("Please try again:\n")
            ViewBuckets()

    file_number = 1
    print("")
    print("*=*" * 14)
    print("\t\t  Current Bucket Files")
    print("*=*" * 14)
    for title in file_titles:
        print(file_number, ":", file_titles[title])
        file_number += 1

    SelectBucketFile(file_titles)


def SelectBucketFile(viewed_file_titles):
    """
    Assigns CLIMenu.selected_filename based on the file selected by the user.
    :param: viewed_file_titles: dictionary of file titles found within current bucket
    :return:
    """
    file_titles = viewed_file_titles

    while True:
        print("\nPlease Select Option:")
        print("",
              "1 - Select Bucket File\n",
              "0 - Exit Bucket File Viewer\n")
        user_input = int(input("Enter Number: "))
        try:
            if user_input < 0 or user_input > 1:
                print("Invalid input: Please try again.")
                raise ValueError
            elif user_input == 0:
                print("Returning to the Main Menu")
                CLIMenu.MainMenu()
            elif user_input == 1:
                chosen_file_number = int(input("Enter the corresponding file number: "))
                if chosen_file_number < 1 or chosen_file_number > len(file_titles):
                    print("Invalid input: Please try again.")
                    SelectBucketFile(file_titles)
                else:
                    chosen_file = file_titles[chosen_file_number]
                    CLIMenu.selected_filename = chosen_file
                    print("\nCurrent filename is now:\n", chosen_file, "\n")
                    break
        except ValueError:  # TODO: Resolve this try-except bug...
            print("Invalid integer. Please enter valid input.")
            #SelectBucketFile(file_titles)

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
                raise ValueError
            elif ok_to_exit == 0:
                CLIMenu.MainMenu()
            elif ok_to_exit == 1:
                CLIMenu.GetUserKeywords()
            elif ok_to_exit == 2:
                ViewBucketFiles(CLIMenu.current_bucket)
        except ValueError:
            print("Invalid integer. Please enter valid input.")
            break


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
