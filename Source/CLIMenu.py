"""
CLI Menu is used to display the DMCT menu at application startup.
It is called by Main.py.
"""
from Source import TextractPDFandDOCXVersion, TextractPNGJPGVersion, ExcelManager
from Source.ManageBuckets import ViewBucketFiles, SelectBucketFile, SelectBucket, ViewBuckets

# These global variables will be referenced within functions below.
current_bucket = None  # Chosen by user with SelectBucket()
selected_filename = None  # Chose by user with SelectBucketFile()T


def MainMenu():
    """
    The Main Menu for the DMCT program that contains submenus for user navigation.
    :return:
    """

    print("*=*" * 14)
    print("Database Management Categorization Tool")
    print("\t" * 2, "(DMCT)")  # <- This version shifts the logo over to fit CLI a little better.
    # print("\t" * 3, " " * 2, "(DMCT)")
    print("*=*" * 14)

    # TODO: Add a constant notifier that shows what bucket user is in.
    # TODO: Add intermediate messages in-between steps to keep user informed.
    flag = True
    while flag is True:
        print("=" * 14, "Main Menu", "=" * 16)
        print("",
              "1 - Input Keyword(s) and Parse Documents\n",
              "2 - View & Select Bucket\n",
              "3 - View & Select Bucket Files\n",
              "4 - Excel Manager\n",
              "0 - Exit DMCT\n\n",
              "Current Bucket: ", current_bucket)
        print("=" * 41)
        user_input = int(input("Enter Number: "))

        try:
            if user_input < 0 or user_input > 4:
                raise ValueError
            elif user_input == 0:
                print("Exiting the Data Management Categorization Tool")
                flag = False
                break
            elif user_input == 1:
                print("\n")
                GetUserKeywords()
            elif user_input == 2:
                print("\n")
                ViewBuckets()
            elif user_input == 3:
                print("\n")
                if current_bucket is None:
                    ViewBuckets()
                else:
                    ViewBucketFiles(current_bucket)
            elif user_input == 4:
                print("\n")
                ExcelManager.ExcelMenu()
            else:
                print("Invalid input: Please try again.")
        except ValueError:
            print("Invalid integer. Please enter valid input.")


def GetUserKeywords():
    """
    Prompts user for keywords and stores them in an array.
    Displays the array to the screen upon completion.
    :return:
    """
    keyword_list = []
    keyword_counter = 0
    global current_bucket
    global selected_filename

    # First, ensure that current bucket and filename are selected.
    if current_bucket is None:
        current_bucket = SelectBucket(ViewBuckets())
    else:
        current_bucket = current_bucket

    if selected_filename is None:
        selected_filename = SelectBucketFile(ViewBuckets())
    else:
        selected_filename = selected_filename

    print("=" * 8, "Keyword Entry Screen", "=" * 11)
    print("(Input '0' when finished)")
    print("=" * 41)

    while True:
        keyword_counter += 1
        user_input = input("Enter keyword # {counter}: ".format(counter=keyword_counter))
        if user_input.lower() == '0':
            break
        else:
            keyword_list.append(user_input.lower())

    keyword_list.sort()
    print("=" * 41)
    print("You've entered the following keyword(s):\n", keyword_list)
    user_input = int(input("Proceed with document tagging?\n"
                           "Enter 1 for 'Yes' or 0 for 'No': "))
    try:
        if user_input < 0 or user_input > 1:
            raise ValueError
        elif user_input == 0:
            print("Would you like to try again?\n",
                  "1 - Try Again\n",
                  "0 - Quit to Main Menu")
            user_input = int(input("Enter Number: "))
            try:
                if user_input < 0 or user_input > 1:
                    raise ValueError
                elif user_input == 0:
                    print("\n")
                    MainMenu()
                elif user_input == 1:
                    print("=" * 41)
                    print("\n")
                    GetUserKeywords()
                else:
                    print("Invalid input: Please try again.")
            except ValueError:
                print("Invalid integer. Please enter a value between 0 and 1.")
        elif user_input == 1:
            if selected_filename.endswith('.jpg') or selected_filename.endswith('.png'):
                TextractPNGJPGVersion.Main(incoming_bucket=current_bucket,
                                           incoming_filename=selected_filename,
                                           incoming_keywords=keyword_list)
            elif selected_filename.endswith('.docx') or selected_filename.endswith('.pdf'):
                TextractPDFandDOCXVersion.Main(incoming_bucket=current_bucket,
                                               incoming_filename=selected_filename,
                                               incoming_keywords=keyword_list)
            else:
                print("DMCT currently only supports the following formats:")
                print("JPG, PNG, PDF, and DOCX")
                ViewBucketFiles(current_bucket)
        else:
            print("Invalid input: Please try again.")
    except ValueError:
        print("Invalid integer. Please enter a value between 0 and 1.")
