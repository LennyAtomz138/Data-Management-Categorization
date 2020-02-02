"""
CLI Menu is used to display the DMCT menu at application startup.
It is called by Main.py.
"""
from Source import TextractPDFVersion


def MainMenu():
    """
    The Main Menu for the DMCT program that contains submenus for user navigation.
    :return:
    """
    while True:
        print("="*14, "Main Menu", "="*16)
        print("",
              "1 - Input Keyword(s) and Parse Documents\n",
              "2 - Input Access Credentials\n",
              "0 - Exit DMCT")
        print("="*41)
        user_input = int(input("Enter Number: "))

        try:
            if user_input < 0 or user_input > 2:
                raise ValueError
            elif user_input == 0:
                print("Exiting the Data Management Categorization Tool")
                break
            elif user_input == 1:
                print("\n")
                GetUserKeywords()
            elif user_input == 2:
                print("\n")
                AccessCredentialsMenu()
            else:
                print("Invalid input: Please try again.")
        except ValueError:
            print("Invalid integer. Please enter a value between 0 and 2.")
    return


def GetUserKeywords():
    """
    Prompts user for keywords and stores them in an array.
    Displays the array to the screen upon completion.
    :return:
    """
    keyword_list = []
    keyword_counter = 0

    print("="*8, "Keyword Entry Screen", "="*11)
    print("(Input 'halt dmct' when finished)")
    print("=" * 41)

    while True:
        keyword_counter += 1
        user_input = input("Enter keyword # {counter}: ".format(counter=keyword_counter))
        if user_input.lower() == 'halt dmct':
            break
        else:
            keyword_list.append(user_input)

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
                    print("\n")
                    GetUserKeywords()
                else:
                    print("Invalid input: Please try again.")
            except ValueError:
                print("Invalid integer. Please enter a value between 0 and 1.")

        elif user_input == 1:
            # TODO: call Textracter HERE!!! <-- TESTING IT NOW!!!
            TextractPDFVersion.Main(keyword_list)
            print("\n")
        else:
            print("Invalid input: Please try again.")
    except ValueError:
        print("Invalid integer. Please enter a value between 0 and 1.")


def AccessCredentialsMenu():
    """
    Used to input access credentials for the `aws configure` terminal command.
    User will need to provide an Access Key and a Secret Key.
    Both of those can be found within their IAM console at aws.amazon.com.
    (IAM console > My Security Credentials > Access Keys)
    :return:
    """
    print("="*8, "Access Credentials Menu", "="*8)

    while True:
        print("",
              "1 - Input Access Credentials\n",
              "0 - Return to the Main Menu")
        print("=" * 41)

        user_input = int(input("Enter Number: "))
        try:
            if user_input < 0 or user_input > 1:
                raise ValueError
            elif user_input == 0:
                print("\n")
                MainMenu()
            elif user_input == 1:
                access_key = input("Input Access Key: ")
                secret_key = input("Input Secret Key: ")
                print("This is still in the test phase.\n")
                print("You entered:\n")
                print("Access Key: ", access_key)
                print("Secret Key: ", secret_key)
                print("\n")
            else:
                print("Invalid input: Enter 0 or 1. \n")
        except ValueError:
            print("Invalid integer. Please enter a value between 0 and 1.")


print("*=*"*14)
print("Database Management Categorization Tool")
print("\t"*3, " "*2, "(DMCT)")
print("*=*"*14)

MainMenu()
